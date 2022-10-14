import base64
import copy
import json
import re
import time as t
import zlib
from datetime import datetime

from prawcore.exceptions import NotFound

from pmtw.constants import (DEFAULT_IDENTIFIER, MAX_WIKI_SIZE, USERNOTES_PAGE,
                            USERNOTES_VERSION)


class ToolboxNote:
	"""Represents a single Toolbox Usernote."""
	def __init__(self, user, note, warning=None, time=None, mod=None, url=None, link='', notes=None):
		"""
		Construtor for the ToolboxNote class.

		Parameters
		----------
		user: String, praw.redditor object
			User the note is being left for
		note: String
			the text of the usernote
		warning: String
			the kind of warning the ntoe should be
		time: Integer
			a unix timestamp in seconds. Optional, will set to current time if
			not specified.
		mod: String, praw.redditor
			the moderator issuing the note. Optional, if not set will be set to
			the user of the praw instance.
		url: String
			url attached to the note. If present, gets converted to a toolbox
			link as `self.link`
		link: String
			the toolbox style short link. if set, will expand to a full url
		notes: ToolboxUsernotes
			if set to a ToolboxUsernotes instance, immediately adds the note.

		"""
		self.user = str(user)
		self.note = note
		self.warning = warning
		self.time = time if time else int(t.time())
		self.human_time = datetime.fromtimestamp(self.time).__str__()
		self.mod = str(mod)
		if link != '': self.link = link
		else: self.link = self.__compress_url(url)
		if url: self.url = url
		else: self.url = self.__expand_link(link)

		if notes != None: notes.add(self)

	def __repr__(self):
		"""praw-style representation of the note."""
		return f"ToolboxNote(user='{self.user}', note='{self.note}', human_time='{self.human_time}')"

	def __dict__(self):
		"""represnts a dict of the note in the format it's stored uncompressed in the json"""
		return {'t': self.time, 'n': self.note, 'm': self.mod, 'w': self.warning, 'l': self.link}

	@staticmethod
	def __expand_link(link):
		"""
		expand toolbox's shortlinks to full urls
		Parameters
		----------
		link: String
			toolbox formatted link to expand to a url
		Returns
		-------
		String
			an expanded link

		"""
		if link == '': return None #if no link, nothing to do
		parts = link.split(',') # 'l,abcde,fghij' format for comments, 'l,kmlno' for links
		if parts[0] == "m": return f'https://reddit.com/message/messages/{parts[1]}'
		if len(parts) > 2: return f'https://reddit.com/comments/{parts[1]}/-/{parts[2]}'
		elif len(parts) > 1: return f'https://reddit.com/{parts[1]}'
		else: return link #modmail links are stored as full links

	@staticmethod
	def __compress_url(url):
		"""
		compress a url to toolbox's `l,` format, if applicable

		Parameters
		----------
			url: String
				url to compress

		Returns
		-------
		String
			the toolbox-formatted link. Recognizes a wide variety of reddit
			links. The following is a non-exhaustive list to give examples:
			https://www.reddit.com/r/subreddit/abcdef/comments/ghijkl/
			http://old.reddit.com/r/subreddit/abcdef/
			http://reddit.com/r/subreddit/abcdef
			http://reddit.com/abcdef
			https://redd.it/abcdef
			reddit.com/abcdef

		"""
		if not url: return '' # If link is empty, nothing to compress
		if url.startswith("l,") or url.startswith("m,"): return url # Link already compressed
		if "mod.reddit" in url: return url # if link is to modmail message, nothing to compress
		match_re = re.compile(r'(https?:\/\/([a-z]{3}\.)?)?redd\.?it(\.com)?\/(r\/[a-z]*\/)?(comments\/)?', re.IGNORECASE)
		if not re.match(match_re, url): raise ValueError(f"cannot format {url}")
		url = re.sub(match_re,"", url)
		url = url.rstrip("/").split("/")
		if len(url) == 3: return f"l,{url[0]},{url[2]}" #return comment link format "l,abcde,fghij"
		else: return f"l,{url[0]}" # Return post link format "l,abcde"


class ToolboxUsernotes:
	"""Represents the Toolbox Usernotes page."""
	
	def __init__(self, subreddit, identifier=DEFAULT_IDENTIFIER, settingsWarnings=[], lazy=False):
		"""
		Construtor for the ToolboxUsernotes class.

		Parameters
		----------
		subreddit: praw.Subreddit object
			The praw object representing the subreddit to pull notes from
		lazy: Bool
			If False, fetch notes from Reddit on instantiation
		identifier: String
			string to identify all actions taken in the wiki save description
		settingsWarnings: List
			Note types which are in Settings which may or may not be present in 
			the usernotes wiki page
		"""
		self.warnings = []
		self.__subreddit = subreddit
		self.__identifier = identifier
		self.__usernotesJSON = {}
		self.__settingsWarnings = settingsWarnings

		if not lazy: self.load()

	def __str__(self):
		"""return the uncompessed json from the usernotes page as a string"""
		return str(self.__usernotesJSON)

	def __repr__(self):
		"""Set display for a ToolboxUsernotes object"""
		return f"ToolboxUsernotes(subreddit='{self.__subreddit}')"

	def __expand_json(self, notes):
		"""
		Private method used to expand the blob portion of usernotes
		
		Parameters
		----------
		notes: Dictionary
			dictionary representing the usernotes JSON

		Returns
		-------
		Dictionary
			dictionary representing the usernotes JSON with blob expanded


		"""
		json_blob = zlib.decompress(base64.b64decode(notes['blob'])).decode('utf-8') # decompress the Blob
		notes.pop('blob', None) # remove the Blob section from the json data	
		notes['users'] = json.loads(json_blob) # add decoded users section to json dictionary
		self.__usernotesJSON = notes
		return notes

	def __compress_json(self, notes=None):
		"""
		Private method to compress json usernotes into a blob for the wiki page
		
		Parameters
		----------
		notes: Dictionary
			usernotes wiki page in dictionary format. Works on self.__usernotesJSON
			if an explicit object is not supplied. This variable exists largely
			for backwards-compatibilty reasons.

		Returns
		-------
		String
			the compressed JSON object, per toolbox's compression methods
		
		"""
		if notes == None: notes = self.__usernotesJSON
		compressed_json = copy.copy(notes) #create a shallow copy of notes
		compressed_json.pop('users', None) #remove the users section from the json data
		blob_data = zlib.compress(json.dumps(notes['users']).encode('utf-8'), 9) #compress blob with zlib
		blob = base64.b64encode(blob_data).decode('utf-8') #encode the blob in base64
		compressed_json['blob'] = blob #insert the blob back into the json
		return json.dumps(compressed_json)

	def __get_warnings(self):
		""""
		Private method. Gets warnings from the usernotes json, and appends
		other available warnings passed to the constructor
		"""
		self.warnings = self.__usernotesJSON['constants']['warnings'].copy()
		if None not in self.warnings: self.warnings.append(None)
		for usernoteColor in self.__settingsWarnings:
			if usernoteColor not in self.warnings:
				self.warnings.append(usernoteColor)
		
	def __get_mod_index(self, mod):
		"""
		Private method. Toolbox stores the moderator as an index for a given 
		note, not the actual name. This method fetches the appropriate unstable 
		index for a given mod, adding the mod to the list of mods if needed.

		Parameters
		----------
		mod: String
			The mod to get the list index for

		Returns
		-------
		Integer
			the integer index of the mod

		"""
		try:
			mod_index = self.__usernotesJSON['constants']['users'].index(mod)
			return mod_index
		except ValueError:
			self.__usernotesJSON['constants']['users'].append(mod)
			return self.__usernotesJSON['constants']['users'].index(mod)

	def __get_warning_index(self, warning):
		"""
		Private method. Toolbox stores warnings as an index for a given 
		note, not the actual warning name. This method fetches the appropriate 
		unstable index for a given warning, adding the warning to the list of 
		warnings in the usernote page if the warning exists in settings but not
		in usernotes.

		Parameters
		----------
		warning: String
			The warning to get the list index for

		Returns
		-------
		Integer
			the integer index of the warning

		Raises
		------
		ValueError
			If the input warning is not valid for these usernotes

		"""
		try:
			warning_index = self.__usernotesJSON['constants']['warnings'].index(warning)
			return warning_index
		except ValueError:
			if warning in self.warnings:
				self.__usernotesJSON['constants']['warnings'].append(warning)
				return self.__usernotesJSON['constants']['warnings'].index(warning)
			else:
				raise ValueError(f"{warning} is not a valid warning.")

	def __match_username(self, username):
		"""
		Try to match a user with notes and get the proper capitalization for key
		""" 
		search_user = ""
		for user in self.list_users():
			if username.lower() == user.lower():
				search_user = user
				break
		if search_user == "":
			search_user = username
		return search_user

	def _save(self, reason='Usernote update'):
		"""
		Save usernotes to Reddit, with whatever reason is specified. Will raise 
		an OverflowError if the current data is too big for the wiki page.

		Parameters
		----------
			reason: String
				Optional, set a custom reason for the wiki page description

		Returns
		-------
		String
			Wiki page update description

		Raises
		------
		OverflowError
			If he text is larger than the allowed 1mb wikipage size
		"""
		reason = f"{reason} {self.__identifier}"
		wikipage_data = self.__compress_json(self.__usernotesJSON)
		if len(wikipage_data) > MAX_WIKI_SIZE:
			raise OverflowError(f'Usernote data {len(wikipage_data) - MAX_WIKI_SIZE} bytes too big to insert')
		self.__subreddit.wiki[USERNOTES_PAGE].edit(content=wikipage_data, reason=reason)
		return reason

	def load(self):
		"""
		Fetch usernotes from Reddit. Initializes a wiki page if the page doesn't 
		currently exist.

		Returns
		-------
		String
			message informing of successful usernote load

		Raises
		------
		RuntimeError
			if the schema doesn't match the expected version.

		"""
		try:
			usernotes = self.__subreddit.wiki[USERNOTES_PAGE].content_md
			notes = json.loads(usernotes)
		except NotFound:
			initialJson = {"ver":USERNOTES_VERSION,"constants":{"users":[],"warnings":self.warnings}, "blob":""}
			self.sub.wiki.create(name=USERNOTES_PAGE, content=initialJson)
			self.sub.wiki[USERNOTES_PAGE].mod.update(listed=False, permlevel=2)
			self.__expand_json(initialJson)
		if notes['ver'] != USERNOTES_VERSION:
			raise RuntimeError(f"Usernotes Schema mismatch. PMTAW requires {USERNOTES_VERSION}, wiki page is {notes['ver']}")
		else:
			self.__expand_json(notes)
			self.__get_warnings()
		return "Usernotes loaded"

	def add(self, note, lazy=False):
		"""
		takes a ToolboxNote object and adds it on Reddit.

		Parameters
		----------
		note: ToolboxNote object
			note to add to the wiki
		timestamp: Int
			if set, delete note with the specified timestamp.
			if not set, delete all usernotes for a given user
		lazy: Bool
			If set to False, will immediately update the wiki page. if set to 
			True, will only modify the local usernote copy for manual saving later.

		Returns
		-------
		String
			string mirroring the description for the wiki update
		Raises
		------
		ValueError
			if the warning specified in the note does not exist in available 
			warning types for the configured subreddit.
		"""
		if lazy == False: self.load()
		
		new_note = note.__dict__()
		if new_note['m'] == 'None':
			new_note['m'] = self.__subreddit._reddit.user.me().name
		if new_note['w'] not in self.warnings:
				raise ValueError(f"{new_note['w']} is not a valid warning type")

		new_note['m'] = self.__get_mod_index(new_note['m'])
		if new_note['w'] == 'None': new_note['w'] = self.__get_warning_index(None)
		else: new_note['w'] = self.__get_warning_index(new_note['w'])

		user = self.__match_username(note.user)
		try:
			self.__usernotesJSON['users'][user]['ns'].insert(0, new_note)
			if lazy == False:
				self._save(f"create new note on user '{user}'")
				return f"create new note on user '{user}'"
		except KeyError:
			self.__usernotesJSON['users'][user] = {'ns': [new_note]}
			if lazy == False:
				self._save(f"create new note on user '{user}'")
				return f"create new note on user '{user}'"

	def remove(self, user, timestamp=-1, lazy=False):
		"""
		removes a specified user note, or all notes for a user. 

		Parameters
		----------
		user: String, praw.redditor
			user to remove notes for
		timestamp: Int
			Optional. if set, delete note with the specified timestamp.
			if not set, delete all usernotes for a given user
		lazy: Bool
			Optional. If set to False, will immediately update the wiki page. if
			set to True, will only modify the local usernote copy for manual 
			saving later.

		Returns
		-------
		String
			string mirroring what's put on the wiki

		Raises
		------
		KeyError
			if the note for the given timestamp isn't found

		"""
		user = str(user)
		user = self.__match_username(user)
		if lazy == False: self.load()

		if timestamp == -1:
			del self.__usernotesJSON['users'][user]
			if lazy == False: self._save(f"Deleted all notes on {user}")
			return f"Deleted all notes on {user}"
		else:
			notes_on_user = self.__usernotesJSON['users'][user]['ns']
			deleted = False
			for i in range(len(notes_on_user)):
				if notes_on_user[i]['t'] == timestamp:
					notes_on_user.pop(i)
					deleted = True
					break
			if deleted == False: raise KeyError(f"failed to find note timestamped {timestamp} for {user}")
			# Delete the user from the database if there are no notes left
			if len(notes_on_user) == 0:
				del self.__usernotesJSON['users'][user]
				if lazy == False: self._save(f"delete all notes on user '{user}'")
				return f"delete all notes on user '{user}'"
			else:
				if lazy == False: self._save(f"delete note {timestamp} on user '{user}'")
				return f"delete note {timestamp} on user '{user}'"

	def list_users(self, lazy=True):
		"""
		Returns a list of all users with notes. If fresh is set to True, will 
		re-load notes from Reddit before listing.

		Parameters
		----------
		lazy: Bool
			if set to False, reload a fresh copy of usernotes before listing

		Returns
		-------
		List
			list of strings of every user with usernotes
		"""
		if lazy == True: self.load()
		return list(self.__usernotesJSON['users'].keys())

	def list_notes(self, user, lazy=True, reverse=False):
		"""
		Returns a list of all notes for the specified user. Case-insensitive

		Parameters
		----------
		user: String, praw.redditor
			user to fetch notes for
		lazy: Bool
			if set to False, reload a fresh copy of usernotes before listing
		reverse: Bool
			if set to True, display newest notes first

		Returns
		-------
		List
			list containing ToolboxUsernotes

		Raises
		------
		KeyError
			if user doesn't exist in usernotes

		"""	
		if lazy == True: self.load()
		user = str(user) #in case a praw user object is passed

		user = self.__match_username(user)

		try:
			users_notes = []
			for note in self.__usernotesJSON['users'][user]['ns']:
				users_notes.append(
					ToolboxNote(
						user = user,
						note = note['n'],
						time = note['t'],
						mod = self.__usernotesJSON['constants']['users'][note['m']],
						warning = self.__usernotesJSON['constants']['warnings'][note['w']],
						link = note['l']
					)
				)
			users_notes = sorted(users_notes, key = lambda x: x.time, reverse=reverse)
			return users_notes
		except KeyError: return []

	def list_all_notes(self, lazy=True, reverse=False):
		"""
		Returns a list of all notes in the wiki

		Parameters
		----------
		lazy: Bool
			if set to True, reload a fresh copy of usernotes before listing
		reverse: Bool
			If True, notes are listed newest to oldest
		Returns
		-------
		List
			list containing ToolboxUsernotes
		"""	
		if lazy == True: self.load()
		notes = []
		for user in self.list_users():
			for note in self.list_notes(user):
				notes.append(note)
		return sorted(notes, key = lambda x: x.time, reverse=reverse)
