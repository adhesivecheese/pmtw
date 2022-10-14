import json
import time as t

from pmtw.usernotes import ToolboxNote, ToolboxUsernotes

"""
Wrappers to provide functionality for users coming from puni
"""

class puni_Note:
	warnings = ['none','spamwatch','spamwarn','abusewarn','ban','permban','botban','gooduser']

	def __init__(self, user, note, subreddit=None, mod=None, link='', warning='none', note_time=int(t.time())):
		self.__n = ToolboxNote(user, note, time=note_time, mod=mod, warning=warning, url=link)
		
		self.username = self.__n.user
		self.note = self.__n.note
		self.subreddit = str(subreddit) if subreddit else None
		self.time = self.__n.time
		self.moderator = self.__n.mod
		self.link = self.__n.link

	def __str__(self):
		return f'{self.username}: {self.note}'

	def __repr__(self):
		return f"Note(username='{self.username}', ver='puni')"

	def full_url(self):
		return self.__n.url

	@staticmethod
	def _compress_url(link):
		return ToolboxNote._ToolboxNote__compress_url(link)

	@staticmethod
	def _expand_url(short_link, subreddit=None):
		if not subreddit: raise ValueError('Subreddit name must be provided')
		return ToolboxNote._ToolboxNote__expand_link(short_link)


class puni_UserNotes:

	schema = 6
	max_page_size = 524288
	zlib_compression_strength = 9
	page_name = 'usernotes'

	def __init__(self, r, subreddit, lazy_start=False):
		self.r = subreddit._reddit
		self.subreddit = subreddit
		self.cached_json = {}
		self.__ToolboxUsernotes = ToolboxUsernotes(self.subreddit, identifier="via puni", settingsWarnings=puni_Note.warnings)

		if not lazy_start: self.get_json()

	def __repr__(self):
		return f"UserNotes(subreddit='{self.subreddit.display_name}')"

	def get_json(self):
		self.__ToolboxUsernotes.load()
		self.cached_json = self.__ToolboxUsernotes._ToolboxUsernotes__usernotesJSON

	def _init_notes(self):
		self.get_json()

	def set_json(self, reason=None, new_page=False):
		if new_page: self.get_json()
		self.__ToolboxUsernotes.save(reason)

	def get_notes(self, user, lazy=False):
		if lazy == True: fresh = False
		else: fresh = True
		return self.__ToolboxUsernotes.list_notes(user, fresh=fresh)

	def get_users(self, lazy=False):
		if lazy == True: fresh = False
		else: fresh = True
		return self.__ToolboxUsernotes.list_users(fresh=fresh)

	def _mod_from_index(self, index):
		return self.__ToolboxUsernotes._ToolboxUsernotes__usernotesJSON['constants']['users'][index]

	def _warning_from_index(self, index):
		return self.__ToolboxUsernotes._ToolboxUsernotes__usernotesJSON['constants']['warnings'][index]

	def _expand_json(self, j):
		return self.__ToolboxUsernotes._ToolboxUsernotes__expand_json(j)

	def _compress_json(self, j):
		return json.loads(self.__ToolboxUsernotes._ToolboxUsernotes__compress_json(j))

	def add_note(self, note, lazy=False):
		self.__ToolboxUsernotes.add(note, lazy)
		self.cached_json = self.__ToolboxUsernotes._ToolboxUsernotes__usernotesJSON
		return f'"create new note on user {note.user}" via puni'

	def remove_note(self, user, index, lazy=False):
		if lazy == True: fresh = False
		else: fresh = True
		idx = 0
		popped = False
		for note in self.__ToolboxUsernotes.list_notes(user, fresh=fresh):
			if idx == index:
				self.__ToolboxUsernotes.remove(user, note.time)
				popped = True
			idx += 1
		if popped:
			self.cached_json = self.__ToolboxUsernotes._ToolboxUsernotes__usernotesJSON
			return f'"delete note #{index} on user {user}" via puni'
		else:
			raise IndexError("pop index out of range")

	def remove_user(self, user, lazy=False):
		if lazy == True: fresh = False
		else: fresh = True
		self.__ToolboxUsernotes.remove(user, fresh=fresh)
		self.cached_json = self.__ToolboxUsernotes._ToolboxUsernotes__usernotesJSON
		return f'"delete user {user} from usernotes" via puni'
