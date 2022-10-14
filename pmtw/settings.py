import json
import urllib.parse
from dataclasses import dataclass
from typing import Any, List

from prawcore.exceptions import NotFound

from pmtw.constants import MAX_WIKI_SIZE, SETTINGS_PAGE, SETTINGS_VERSION, DEFAULT_IDENTIFIER


class JSONEncoder(json.JSONEncoder):
	# overload method default
	def default(self, obj):
		if isinstance(obj, ModMacro): return obj.to_dict()
		elif isinstance(obj, Reason): return obj.to_dict()
		elif isinstance(obj, RemovalReasons): return obj.to_dict()
		return obj.__dict__


@dataclass
class BanMacros:
	banNote: str
	banMessage: str

	@staticmethod
	def from_dict(obj: Any) -> 'BanMacros':
		_banNote = str(obj.get("banNote"))
		_banMessage = str(obj.get("banMessage"))
		return BanMacros(_banNote, _banMessage)


@dataclass
class DomainTag:
	name: str
	color: str

	@staticmethod
	def from_dict(obj: Any) -> 'DomainTag':
		_name = str(obj.get("name"))
		_color = str(obj.get("color"))
		return DomainTag(_name, _color)


@dataclass
class ModMacro:
	text: str
	title: str
	distinguish: bool
	ban: bool
	mute: bool
	remove: bool
	approve: bool
	lockthread: bool
	lockreply: bool
	sticky: bool
	archivemodmail: bool
	highlightmodmail: bool
	contextpost: bool
	contextcomment: bool
	contextmodmail: bool

	def to_dict(ModMacro):
		d = {
			"text":urllib.parse.quote(ModMacro.text),
			"title": ModMacro.title,
			"distinguish": ModMacro.distinguish,
			"ban": ModMacro.ban,
			"mute": ModMacro.mute,
			"remove": ModMacro.remove,
			"approve": ModMacro.approve,
			"lockthread": ModMacro.lockthread,
			"lockreply": ModMacro.lockreply,
			"sticky": ModMacro.sticky,
			"archivemodmail": ModMacro.archivemodmail,
			"highlightmodmail": ModMacro.highlightmodmail,
			"contextpost": ModMacro.contextpost,
			"contextcomment": ModMacro.contextcomment,
			"contextmodmail": ModMacro.contextmodmail
		}
		return d

	@staticmethod
	def from_dict(obj: Any) -> 'ModMacro':
		_text = urllib.parse.unquote(str(obj.get("text")))
		_title = str(obj.get("title"))
		_distinguish = bool(obj.get("distinguish"))
		_ban = bool(obj.get("ban"))
		_mute = bool(obj.get("mute"))
		_remove = bool(obj.get("remove"))
		_approve = bool(obj.get("approve"))
		_lockthread = bool(obj.get("lockthread"))
		_lockreply = bool(obj.get("lockreply"))
		_sticky = bool(obj.get("sticky"))
		_archivemodmail = bool(obj.get("archivemodmail"))
		_highlightmodmail = bool(obj.get("highlightmodmail"))
		_contextpost = bool(obj.get("contextpost"))
		_contextcomment = bool(obj.get("contextcomment"))
		_contextmodmail = bool(obj.get("contextmodmail"))
		return ModMacro(_text, _title, _distinguish, _ban, _mute, _remove, _approve, _lockthread, _lockreply, _sticky, _archivemodmail, _highlightmodmail, _contextpost, _contextcomment, _contextmodmail)


@dataclass
class Reason:
	text: str
	flairText: str
	flairCSS: str
	removePosts: bool
	removeComments: bool
	title: str
	flairTemplateID: str

	def to_dict(Reason):
		d = {
			"text": urllib.parse.quote(Reason.text),
			"flairText": Reason.flairText,
			"flairCSS": Reason.flairCSS,
			"removePosts": Reason.removePosts,
			"removeComments": Reason.removeComments,
			"title": Reason.title,
			"flairTemplateID": Reason.flairTemplateID
		}
		return d

	@staticmethod
	def from_dict(obj: Any) -> 'Reason':
		_text = urllib.parse.unquote(str(obj.get("text")))
		_flairText = str(obj.get("flairText"))
		_flairCSS = str(obj.get("flairCSS"))
		_removePosts = bool(obj.get("removePosts"))
		_removeComments = bool(obj.get("removeComments"))
		_title = str(obj.get("title"))
		_flairTemplateID = str(obj.get("flairTemplateID"))
		return Reason(_text, _flairText, _flairCSS, _removePosts, _removeComments, _title, _flairTemplateID)


@dataclass
class RemovalReasons:
	pmsubject: str
	logreason: str
	header: str
	footer: str
	removalOption: str
	typeReply: str
	typeStickied: bool
	typeCommentAsSubreddit: bool
	typeLockComment: bool
	typeAsSub: bool
	autoArchive: bool
	typeLockThread: bool
	logsub: str
	logtitle: str
	bantitle: str
	getfrom: str
	reasons: List[Reason]

	def to_dict(RemovalReasons):
		d = {
		"pmsubject": urllib.parse.quote(RemovalReasons.pmsubject),
		"logreason": urllib.parse.quote(RemovalReasons.logreason),
		"header": urllib.parse.quote(RemovalReasons.header),
		"footer": urllib.parse.quote(RemovalReasons.footer),
		"removalOption": RemovalReasons.removalOption,
		"typeReply": RemovalReasons.typeReply,
		"typeStickied": RemovalReasons.typeStickied,
		"typeCommentAsSubreddit": RemovalReasons.typeCommentAsSubreddit,
		"typeLockComment": RemovalReasons.typeLockComment,
		"typeAsSub": RemovalReasons.typeAsSub,
		"autoArchive": RemovalReasons.autoArchive,
		"typeLockThread": RemovalReasons.typeLockThread,
		"logsub": urllib.parse.quote(RemovalReasons.logsub),
		"logtitle":RemovalReasons.logtitle,
		"bantitle": urllib.parse.quote(RemovalReasons.bantitle),
		"getfrom": RemovalReasons.getfrom,
		"reasons":[Reason.to_dict(r) for r in RemovalReasons.reasons]
		}
		return d

	@staticmethod
	def from_dict(obj: Any) -> 'RemovalReasons':
		_pmsubject = urllib.parse.unquote(str(obj.get("pmsubject")))
		_logreason = urllib.parse.unquote(str(obj.get("logreason")))
		_header = urllib.parse.unquote(str(obj.get("header")))
		_footer = urllib.parse.unquote(str(obj.get("footer")))
		_removalOption = str(obj.get("removalOption"))
		_typeReply = str(obj.get("typeReply"))
		_typeStickied = bool(obj.get("typeStickied"))
		_typeCommentAsSubreddit = bool(obj.get("typeCommentAsSubreddit"))
		_typeLockComment = bool(obj.get("typeLockComment"))
		_typeAsSub = bool(obj.get("typeAsSub"))
		_autoArchive = bool(obj.get("autoArchive"))
		_typeLockThread = bool(obj.get("typeLockThread"))
		_logsub = urllib.parse.unquote(str(obj.get("logsub")))
		_logtitle = str(obj.get("logtitle"))
		_bantitle = urllib.parse.unquote(str(obj.get("bantitle")))
		_getfrom = str(obj.get("getfrom"))
		_reasons = [Reason.from_dict(y) for y in obj.get("reasons")]
		return RemovalReasons(_pmsubject, _logreason, _header, _footer, _removalOption, _typeReply, _typeStickied, _typeCommentAsSubreddit, _typeLockComment, _typeAsSub, _autoArchive, _typeLockThread, _logsub, _logtitle, _bantitle, _getfrom, _reasons)


@dataclass
class UsernoteColor:
	key: str
	text: str
	color: str

	@staticmethod
	def from_dict(obj: Any) -> 'UsernoteColor':
		_key = str(obj.get("key"))
		_text = str(obj.get("text"))
		_color = str(obj.get("color"))
		return UsernoteColor(_key, _text, _color)


@dataclass
class SettingsRoot:
	ver: int
	domainTags: List[DomainTag]
	removalReasons: RemovalReasons
	modMacros: List[ModMacro]
	usernoteColors: List[UsernoteColor]
	banMacros: BanMacros

	def __repr__(self):
		return f"SettingsRoot(ver='{self.ver}')"

	def __str__(self):
		return self.to_json()

	def to_json(self):
		return json.dumps(self.__dict__, cls=JSONEncoder)

	@staticmethod
	def from_dict(obj: Any) -> 'SettingsRoot':
		_ver = int(obj.get("ver"))
		_domainTags = [DomainTag.from_dict(y) for y in obj.get("domainTags")]
		_removalReasons = RemovalReasons.from_dict(obj.get("removalReasons"))
		_modMacros = [ModMacro.from_dict(y) for y in obj.get("modMacros")]
		_usernoteColors = [UsernoteColor.from_dict(y) for y in obj.get("usernoteColors")]
		_banMacros = BanMacros.from_dict(obj.get("banMacros"))
		return SettingsRoot(_ver, _domainTags, _removalReasons, _modMacros, _usernoteColors, _banMacros)


class ToolboxSettings:
	"""Represents the Toolbox Settings page."""
	def __init__(self, subreddit, identifier=DEFAULT_IDENTIFIER, lazy=False):
		"""
		Construtor for the ToolboxSettings class.

		Parameters
		----------
		subreddit: praw.subreddit object
			the subreddit to use the Toolbox object with
		lazy: Bool
			if set to True, does not fetch from Reddit on instantiation
		identifier: String
			string that get's appended to all wikiedit discriptions identifying
			pmtw as the actioner. Defaults to "via pmtw"
		"""
		
		self.__subreddit = subreddit
		self.identifier = identifier
		self.__settings = ""
		self.ver = ""
		self.domainTags = ""
		self.removalReasons = ""
		self.modMacros = ""
		self.usernoteColors = ""
		self.banMacros = ""
		self.warnings = ""

		if not lazy: self.load()

	def __repr__(self):
		"""Set display for a ToolboxSettings object"""
		return f"ToolboxSettings(subreddit='{self.__subreddit}')"

	def load(self):
		"""
		Load Toolbox Settings from Reddit

		Returns
		-------
		String
			Information letting the user know settings are loaded
		"""

		try:
			page = self.__subreddit.wiki[SETTINGS_PAGE].content_md
			page = json.loads(page)
			if page["ver"] != 1: raise ValueError(f"pmtw requires settings ver {SETTINGS_VERSION}, got {page['ver']}")
		except NotFound:
			initialJSON = {"ver":1,"domainTags":"","removalReasons":{"pmsubject":"","logreason":"","header":"test","footer":"","removalOption":"suggest","typeReply":"reply","typeStickied":False,"typeCommentAsSubreddit":False,"typeLockComment":False,"typeAsSub":False,"autoArchive":False,"typeLockThread":False,"logsub":"","logtitle":"","bantitle":"","getfrom":"","reasons":[]},"modMacros":[],"usernoteColors":[{"key":"gooduser","text":"Good Contributor","color":"#008000"},{"key":"spamwatch","text":"Spam Watch","color":"#ff00ff"},{"key":"spamwarn","text":"Spam Warning","color":"#800080"},{"key":"abusewarn","text":"Abuse Warning","color":"#ffa500"},{"key":"ban","text":"Ban","color":"#ff0000"},{"key":"permban","text":"Permanent Ban","color":"#8b0000"},{"key":"botban","text":"Bot Ban","color":"#000000"}],"banMacros":{"banNote":"","banMessage":""}}
			page = self.__subreddit.wiki.create(name=SETTINGS_PAGE, content=str(initialJSON))
			self.__subreddit.wiki[SETTINGS_PAGE].mod.update(listed=False, permlevel=2)

		# append expected items to the json, in case the toolbox settings 
		# don't have them, since things get added here without a bump to ver
		for item in ["domainTags", "removalReasons", "modMacros","banMacros"]:
			if item not in page.keys(): page[item] = ""

		# Copy things over so we don't have to hit ToolboxSettings.settings
		# for every variable
		self.__settings = SettingsRoot.from_dict(page)
		self.ver = self.__settings.ver
		self.domainTags = self.__settings.domainTags
		self.removalReasons = self.__settings.removalReasons
		self.modMacros = self.__settings.modMacros
		self.usernoteColors = self.__settings.usernoteColors
		self.banMacros = self.__settings.banMacros

		warnings = []
		for color in self.usernoteColors:
			warnings.append(color.key)
		self.warnings = warnings

		return "Settings loaded"

	def save(self, reason="Settings update"):
		"""
		Save Toolbox settings back to Reddit

		Parameters
		----------
		reason: String
			Optional, set a custom reason for the wiki page description

		Returns
		-------
		String
			Reason with identifier set when instantiating a Toolbox object

		Raises
		------
		OverflowError
			If the settings page is too big to save to Reddit

		"""
		reason = f"{reason} {self.identifier}"

		# Copy the class variables back to the dataclasses for compression
		self.__settings.ver = self.ver
		self.__settings.domainTags = self.domainTags
		self.__settings.removalReasons = self.removalReasons
		self.__settings.modMacros = self.modMacros
		self.__settings.usernoteColors = self.usernoteColors
		self.__settings.banMacros = self.banMacros

		if len(self.__settings.__str__()) > MAX_WIKI_SIZE:
			raise OverflowError(f'Usernote data {len(self.__settings.__str__()) - MAX_WIKI_SIZE} bytes too big to insert')
		self.__subreddit.wiki[SETTINGS_PAGE].edit(content=self.__settings.__str__(),reason=reason)
		return reason
