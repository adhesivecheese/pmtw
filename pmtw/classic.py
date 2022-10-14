import json
import urllib.parse

from pmtw.usernotes import ToolboxNote, ToolboxUsernotes
from pmtw.toolbox import Toolbox

"""
Wrappers to provide drop-in functionality for users coming from pmtw version 0.2.1
"""

class Note:
	"""
	Wrapper for ToolboxNote, to act as a drop-in replacement for 
	pmtw version 0.2.1
	"""
	def __init__(self, user, note, time=None, mod=None, warning=None, link='', subreddit=None):
		self.__n = ToolboxNote(user, note, time=time, mod=mod, warning=warning, url=link)
		self.user = self.__n.user
		self.time = self.__n.time
		self.note = self.__n.note
		self.mod = self.__n.mod
		self.warning = self.__n.warning
		self.subreddit = subreddit

		if "l," in self.__n.link:
			self.link = f"https://redd.it/{self.__n.link.split(',')[1]}"
		else:
			self.link = link

	def __repr__(self):
		return f"Note(user='{self.user}', note='{self.note}', time='{self.time}')"


class Usernotes:
	"""
	Wrapper for ToolboxUsernotes, to act as a drop-in replacement for 
	pmtw version 0.2.1
	"""
	def __init__(self, r, subreddit, fetch=True):
		self.r = subreddit._reddit
		self.subreddit = subreddit
		self.usernotesJSON = {}
		self.__ToolboxUsernotes = ToolboxUsernotes(self.subreddit, identifier="via pmtw")

		if fetch == True:
			self.__ToolboxUsernotes.load()
			self.usernotesJSON = self.__ToolboxUsernotes._ToolboxUsernotes__usernotesJSON

	def __repr__(self):
		return f"Usernotes(subreddit='{self.subreddit}')"

	def __mod_index(self, mod, type="decode"):
		if type == "decode":
			return self.usernotesJSON['constants']['users'][mod]
		else:
			return self.__ToolboxUsernotes._ToolboxUsernotes__get_mod_index(mod)

	def __warnings_index(self, warning, type ="decode"):
		if type == "decode":
			return self.__ToolboxUsernotes.warnings.index(warning)
		else:
			return self.__ToolboxUsernotes._ToolboxUsernotes__get_warning_index(warning)

	def __expand_json(self, notes):
		return self.__ToolboxUsernotes._ToolboxUsernotes__expand_json(notes)
	
	def __compress_json(self, notes):
		return json.loads(self.__ToolboxUsernotes._ToolboxUsernotes__compress_json(notes))

	def __fetch_from_reddit(self):
		self.__ToolboxUsernotes.load()

	def __expand_link(self, link):
		return ToolboxNote._ToolboxNote__expand_link(link)

	def __compress_link(self, link):
		print(link)
		l = ToolboxNote._ToolboxNote__compress_url(link)
		return l

	def push_usernotes(self, reason='"Batch usernote update"', truncate=False):
		self.__ToolboxUsernotes.save(reason=reason)
	
	def warnings_types(self, local=True):
		if local == False: self.__ToolboxUsernotes.load()
		return self.__ToolboxUsernotes.warnings

	def get_user_notes(self, user, local=True):
		if local == True: fresh = False
		else: fresh = True
		return self.__ToolboxUsernotes.list_notes(user,fresh=fresh)

	def existing_users(self, local=True):
		if local == True: fresh = False
		else: fresh = True
		return self.__ToolboxUsernotes.list_users(fresh=fresh)

	def add_note(self, note, batch=False):
		print(note._Note__n.url) #preserve quirk with version 0.2.1
		if note.warning not in self.__ToolboxUsernotes.warnings:
			raise ValueError(f"{note.warning} is not a valid warning kind.")
		return self.__ToolboxUsernotes.add(note._Note__n, bulk_action=batch)

	def delete_note(self, username, timestamp, batch=False):
		return self.__ToolboxUsernotes.remove(username, timestamp, bulk_action=batch)

	def purge_user_notes(self, username, batch=False):
		return self.__ToolboxUsernotes.remove(username, bulk_action=batch)


class Settings:
	"""
	Wrapper for ToolboxSettings, to act as a drop-in replacement for 
	pmtw version 0.2.1
	"""
	def __init__(self, r, subreddit, fetch=True):
		self.r = subreddit._reddit
		self.subreddit = subreddit
		self.settingsJSON = {}
		self.__Toolbox = Toolbox(subreddit)

		if fetch:
			self.__Toolbox.load_settings()
			self.settingsJSON = self.__Toolbox.settings

	def __repr__(self):
		return f"ToolboxSettings(subreddit='{self.subreddit}')"

	def __decode_text(self,text):
		return urllib.parse.unquote(text)

	def __encode_text(self, text):
		return urllib.parse.quote(text)
	
	def __fetch_from_reddit(self):
		self.__Toolbox.load_settings()

	def push_settings(self, reason='Toolbox Settings update from pmtw'):
		self.__Toolbox.save_settings()

	def test(self):
		return self.settingsJSON

	def get_domainTags(self, local=True):
		if local == False: self.__Toolbox.load_settings()
		return self.__Toolbox.settings.domainTags

	def get_removalReasons(self, local=True):
		if local == False: self.__Toolbox.load_settings()
		return self.__Toolbox.settings.removalReasons

	def get_reasons(self, local=True):
		if local == False: self.__Toolbox.load_settings()
		self.__Toolbox.settings.removalReasons.reasons

	def add_reason(self, reason, local=True):
		if local == False: self.__Toolbox.load_settings()
		self.__Toolbox.settings.removalReasons.reasons.append(reason)

	def get_modMacros(self, local=True):
		if local == False: self.__Toolbox.load_settings()
		return self.__Toolbox.settings.modMacros

	def get_usernoteColors(self, local=True):
		if local == False: self.__Toolbox.load_settings()
		return self.__Toolbox.settings.usernoteColors

	def get_banMacros(self, local=True):
		if local == False: self.__Toolbox.load_settings()
		return self.__Toolbox.settings.banMacros
