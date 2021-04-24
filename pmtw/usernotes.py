import praw
import json
import re
import zlib
import base64
import copy
import time as t
from prawcore.exceptions import NotFound
from pmtw.decorators import batch, localdata
from pmtw.constants import usernotes_schema, usernotes_page, zlib_compression_strength, max_wiki_size


# Note represents an individual usernote
class Note(object):
	def __init__(self, user, note, time=None, mod=None, warning=None, link='', subreddit=None):
			self.user = user
			self.time = time if time else int(t.time())
			self.note = note
			self.mod = mod
			self.warning = warning
			self.link = link
			self.subreddit = subreddit

	def __repr__(self):
		return f"Note(user='{self.user}', note='{self.note}', time='{self.time}')"


# Usernotes represents the usernotes wiki page
class Usernotes(object):
	"""
		Construtor for the Usernotes class. Arguments:
		* r: The praw object representing the authenticated Reddit instance.
		* subreddit: The praw object representing the subreddit to pull notes from
		* fetch: Boolean, whether to grab notes on instantiation
	"""
	def __init__(self, r, subreddit, fetch=True):
		self.r = r
		self.subreddit = subreddit
		self.usernotesJSON = {}

		if fetch == True: self.__fetch_from_reddit()

	"""Set display for a Usernotes object"""
	def __repr__(self):
		return f"Usernotes(subreddit='{self.subreddit}')"


	"""Private method to encode or decode the number representing a mod"""
	def __mod_index(self, mod, type="decode"):
		if type == "decode": return self.usernotesJSON['constants']['users'][mod]
		else: return self.usernotesJSON['constants']['users'].index(mod)


	"""Private method to encode or decode the number representing a warning"""
	def __warnings_index(self, warning, type ="decode"):
		if type == "decode": return self.usernotesJSON['constants']['warnings'][warning]
		else: return self.usernotesJSON['constants']['warnings'].index(warning)


	"""Private method used to expand the blob portion of usernotes"""
	def __expand_json(self, notes):
		expanded_json = copy.copy(notes) #create a shallow copy of notes
		expanded_json.pop('blob', None) # remove the Blob section from the json data
		json_blob = zlib.decompress(base64.b64decode(notes['blob'])).decode('utf-8') # decompress the Blob
		expanded_json['users'] = json.loads(json_blob) # add decoded users section to json dictionary
		return expanded_json


	"""Private method to compress json usernotes into a blob for the wiki page"""
	def __compress_json(self, notes):
		compressed_json = copy.copy(notes) #create a shallow copy of notes
		compressed_json.pop('users', None) #remove the users section from the json data

		blob_data = zlib.compress(
			json.dumps(notes['users']).encode('utf-8'),
			zlib_compression_strength
		) #compress blob with zlib
		blob = base64.b64encode(blob_data).decode('utf-8') #encode the blob in base64
		compressed_json['blob'] = blob #insert the blob back into the json
		return compressed_json


	"""Private method to fetch usernotes from Reddit"""
	def __fetch_from_reddit(self):
		try:
			usernotes = self.subreddit.wiki[usernotes_page].content_md
			notes = json.loads(usernotes)
		except NotFound:
			raise RuntimeError("Usernotes page does not exist")
		if notes['ver'] != usernotes_schema:
			raise RuntimeError(f"Usernotes Schema mismatch. PMTAW requires {usernotes_schema}, wiki page is {notes['ver']}")
		else:
			self.usernotesJSON = self.__expand_json(notes)
		return self.usernotesJSON


	"""Private method which expands toolbox links into actual urls"""
	def __expand_link(self, link):
		if link == '': return None #if no link, nothing to do
		parts = link.split(',') # 'l,abcde,fghij' format for comments, 'l,kmlno' for links
		if len(parts) > 2: return f'https://reddit.com/r/{self.subreddit}/comments/{parts[1]}/-/{parts[2]}'
		elif len(parts) > 1: return f'https://reddit.com/{parts[1]}'
		else: return link #modmail links are stored as full links


	"""Private method to compress links into toolbox versions"""
	def __compress_link(self, link):
		print(link)
		if link == '': return '' # If link is empty, nothing to compress
		if "mod.reddit" in link: return link # if link is to modmail message, nothing to compress
		if f"r/{self.subreddit}/comments/" in link:
			comment_re = re.compile(r'/comments/([A-Za-z\d]{2,})(?:/[^\s]+/([A-Za-z\d]+))?')
			matches = re.findall(comment_re, link)[0]
			return f'l,{matches[0]},{matches[1]} ' #return comment link format "l,abcde,fghij"
		return f"l,{link.split('/')[3]}" # Return post link format "l,abcde"


	"""Method to push usernotes back to Reddit"""
	def push_usernotes(self, reason='"Batch usernote update" via pmtw', truncate=False):
		wikipage_data = json.dumps(self.__compress_json(self.usernotesJSON))
		usernotes_max_wiki_size = max_wiki_size * 2
		if len(wikipage_data) > usernotes_max_wiki_size:
			#TODO: if truncate is true, truncate oldest usernotes to fit if too big
			raise OverflowError(f'Usernote data {len(wikipage_data) - usernotes_max_wiki_size} bytes too big to insert')
		try: self.subreddit.wiki[usernotes_page].edit(wikipage_data, reason)
		except: self.r.request("POST", path=f"/r/{self.subreddit}/api/wiki/edit", data={"content": wikipage_data, "page":"usernotes", "reason":reason})
		return


	"""
	Return warning types of notes on userpage. Use 
	warnings_types(local="False") to fetch notes
	from Reddit before listing warnings
	"""
	@localdata
	def warnings_types(self):
		#TODO: return warnings from settings page instead
		#That way we get all available warnings, not just
		#those currently in use
		return self.usernotesJSON['constants']['warnings']


	"""
	Returns a list of Note objects for a user. Case-insensitive.
	Use get_user_notes(local="False") to fetch notes from Reddit
	fetching notes
	"""
	@localdata
	def get_user_notes(self, user):
		user = str(user) #in case a praw user object is passed

		# Try to match a user with notes and get the proper capitalization for key
		extant_users = self.existing_users()
		search_user = ""
		for nuser in extant_users:
			if user.lower() == nuser.lower(): search_user = nuser
		if search_user == "": search_user = user

		try:
			users_notes = []
			for note in self.usernotesJSON['users'][search_user]['ns']:
				users_notes.append(
					Note(
						user = user,
						note = note['n'],
						time = note['t'],
						mod = self.__mod_index(note['m']),
						warning = self.__warnings_index(note['w']),
						link = self.__expand_link(note['l']),
						subreddit = self.subreddit
					)
				)
			return users_notes
		except KeyError: return []


	"""
	Returns list of usernames that have notes.
	Use existing_users(local="False") to fetch notes before
	returning list of users
	"""
	@localdata
	def existing_users(self):
		return list(self.usernotesJSON['users'].keys())


	"""
	Add a note to a user on Reddit. Accepts a Note object
	By default, immediately adds to wiki page. You can override
	immediate insertion by passing add_note(note, batch="True");
	if so, you will need to manually sync notes with push_usernotes() 
	"""
	@batch
	def add_note(self, note):
		notes = self.usernotesJSON
		if not note.mod: note.mod = self.r.user.me().name
		try: mod_index = self.__mod_index(note.mod, "encode")
		except ValueError:
			notes['constants']['users'].append(note.mod)
			mod_index = notes['constants']['users'].index(note.mod)
		try:
			if note.warning in self.warnings_types():
				 warning_index = self.__warnings_index(note.warning, "encode")
		except:
			raise ValueError(f"{note.warning} is not a valid warning kind.")
		if note.link: link = self.__compress_link(note.link)
		new_note = {
			't': note.time, 'n': note.note, 'm': mod_index,
			'w': warning_index, 'l': link
		}
		try:
			notes['users'][note.user]['ns'].insert(0, new_note)
			return f"\"create new note on user '{note.user}'\" via pmtw"
		except KeyError:
			notes['users'][note.user] = {'ns': [new_note]}
			return f"\"create new note on new user '{note.user}'\" via pmtw"

	"""
	Delete a note on a user. Requires a username, and the timestamp of
	the note to delete.	By default, immediately updates wiki page. You
	can override immediate update by passing delete_note(note, batch="True");
	if so, you will need to manually sync notes with push_usernotes() 
	"""
	@batch
	def delete_note(self, username, timestamp):
		notes_on_user = self.usernotesJSON['users'][username]['ns']
		for i in range(len(notes_on_user)):
			if notes_on_user[i]['t'] == timestamp:
				notes_on_user.pop(i)
				break
		# Delete the user from the database if there are no notes left
		if len(notes_on_user) == 0:
			#respect batch mode
			if batch == True: self.purge_user_notes(username, immediate=True)
			else: self.purge_user_notes(username)
			return
		else:
			#multiplication of timestamp is for consistency with toolbox display
			return f"\"delete note {timestamp*10000} on user '{username}'\" via pmtw"


	"""
	Delete all notes on a user. Requires a username. By default, immediately updates
	the wiki page. You can override this behavior by passing purge_user_notes(user, batch="True");
	if so, you will manually need to manually sync notes with push_usernotes()
	"""
	@batch
	def purge_user_notes(self, username, immediate=False):
		del self.usernotesJSON['users'][username]
		if immediate == True: self.push_usernotes(f"\"delete all notes on user '{username}'\" via pmtw")
		return f"\"delete all notes on user '{username}'\" via pmtw"
