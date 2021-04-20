import json
import copy
import urllib.parse
from prawcore.exceptions import NotFound
from .constants import settings_schema, settings_page, max_wiki_size
from pmtw.decorators import localdata

"""Represents a single Domain Tag"""
class domainTag(object):
	def __init__(self, name, color):
			self.name  = name
			self.color = color

	def __repr__(self):
		return f"domainTag(user='{self.name}', time='{self.color}')"


"""
Represents the Removal Reasons section.
Contains removal reasons as reason objects.
"""
class removalReason(object):
	def __init__(self, pmsubject, logreason, header, footer, removalOption, typeReply, typeStickied, typeLockComment, typeAsSub, autoArchive, typeLockThread, logsub, logtitle, bantitle, getfrom, reasons):
			self.pmsubject       = pmsubject
			self.logreason       = logreason
			self.header          = header
			self.footer          = footer
			self.removalOption   = removalOption
			self.typeReply       = typeReply
			self.typeStickied    = typeStickied
			self.typeLockComment = typeLockComment
			self.typeAsSub       = typeAsSub
			self.autoArchive     = autoArchive
			self.typeLockThread  = typeLockThread
			self.logsub          = logsub
			self.logtitle        = logtitle
			self.bantitle        = bantitle
			self.getfrom         = getfrom
			self.reasons         = reasons

	def __repr__(self):
		return f"removalReasons()"

"""Represents a single removal reason"""
class reason(object):
	def __init__(self, title, text, flairText, flairCSS, removePosts, removeComments):
		self.text           = text
		self.flairText      = flairText
		self.flairCSS       = flairCSS
		self.title          = title
		self.removePosts    = removePosts
		self.removeComments = removeComments

	def __repr__(self):
		return f"reason(title='{self.title})'"

"""Represents a single mod macro"""
class modMacro(object):
	def __init__(self, text, title, distinguish, ban, mute, remove, approve, lockthread, lockreply, sticky, archivemodmail, highlightmodmail, contextpost, contextcomment, contextmodmail):
			self.text = text
			self.title = title
			self.distinguish = distinguish
			self.ban = ban
			self.mute = mute
			self.remove = remove
			self.approve = approve
			self.lockthread = lockthread
			self.lockreply = lockreply
			self.sticky = sticky
			self.archivemodmail = archivemodmail
			self.highlightmodmail = highlightmodmail
			self.contextpost = contextpost
			self.contextcomment = contextcomment
			self.contextmodmail = contextmodmail

	def __repr__(self):
		return f"modMacro(title='{self.title}')"


"""Represents a single usernote color"""
class usernoteColor(object):
	def __init__(self, key, text, color):
			self.key   = key
			self.text  = text
			self.color = color

	def __repr__(self):
		return f"usernoteColor(key='{self.key}', text='{self.text}', color='{self.color}')"


"""Represents a single ban macro"""
class banMacro(object):
	def __init__(self, banNote, banMessage):
			self.banNote    = banNote
			self.banMessage = banMessage

	def __repr__(self):
		return f"banMacro(banNote='{self.banNote}', banMessage='{self.banMessage}')"

"""Represents the Settings page for toolbox, for subreddit settings"""
class Settings(object):
	def __init__(self, r, subreddit, fetch=True):
		self.r = r
		self.subreddit = subreddit
		self.settingsJSON = {}

		if fetch:
			self.__fetch_from_reddit()


	"""Set display for Settings object"""
	def __repr__(self):
		return f"ToolboxSettings(subreddit='{self.subreddit}')"


	"""Private method. Some strings are stored encoded in settings"""
	def __decode_text(self,text):
		return urllib.parse.unquote(text)


	"""Private method to reencode strings which should be stored encoded"""
	def __encode_text(self, text):
		return urllib.parse.quote(text.encode("utf-8"))


	"""Private method to fetch toolbox settings"""
	def __fetch_from_reddit(self):
		try:
			settings = self.subreddit.wiki[settings_page].content_md
			settings = json.loads(settings)
		except NotFound:
			raise RuntimeError("Toolbox settings page does not exist")
		if settings['ver'] != settings_schema:
			raise RuntimeError(f"Settings Schema mismatch. PMTW requires {settings_schema}, wiki page is {settings['ver']}")
		else:
			self.settingsJSON = settings
		return self.settingsJSON


	"""Method to update Toolbox Settings page"""
	def push_settings(self, reason='Toolbox Settings update from pmtw'):
		wikipage_data = json.dumps(self.settingsJSON)
		if len(wikipage_data) > max_wiki_size:
			raise OverflowError(f'settings data {len(wikipage_data) - max_wiki_size} bytes too big to insert')
		self.subreddit.wiki[settings_page].edit(wikipage_data, reason)
		return


	def test(self):
		return self.settingsJSON

	"""
	Get domain tags as a list. Use get_domainTags(local="False")
	to fetch from Reddit before retrieval.
	"""
	@localdata
	def get_domainTags(self):
		domainTags = []
		try:
			for item in self.settingsJSON['']:
				domainTags.append(
					domainTag(
						name  = item['name']  if 'name'  in item.keys() else None,
						color = item['color'] if 'color' in item.keys() else None
					)
				)
		except KeyError: raise KeyError("Section ['domainTags'] does not seem to exist in settings")
		return domainTags


	"""
	Get Removal Reasons information as a list. Use
	get_removalReasons(local="False") to fetch from Reddit before returning.
	"""
	@localdata
	def get_removalReasons(self):
		removalReasons = []
		try:
			item = self.settingsJSON['removalReasons']
			removalReasons.append(
				removalReason(
					pmsubject       = item['pmsubject']                  if 'pmsubject'       in item.keys() else None,
					logreason       = item['logreason']                  if 'logreason'       in item.keys() else None,
					header          = self.__decode_text(item['header']) if 'header'          in item.keys() else None,
					footer          = self.__decode_text(item['footer']) if 'footer'          in item.keys() else None,
					removalOption   = item['removalOption']              if 'removalOption'   in item.keys() else None,
					typeReply       = item['typeReply']                  if 'typeReply'       in item.keys() else None,
					typeStickied    = item['typeStickied']               if 'typeStickied'    in item.keys() else None,
					typeLockComment = item['typeLockComment']            if 'typeLockComment' in item.keys() else None,
					typeAsSub       = item['typeAsSub']                  if 'typeAsSub'       in item.keys() else None,
					autoArchive     = item['autoArchive']                if 'autoArchive'     in item.keys() else None,
					typeLockThread  = item['typeLockThread']             if 'typeLockThread'  in item.keys() else None,
					logsub          = item['logsub']                     if 'logsub'          in item.keys() else None,
					logtitle        = item['logtitle']                   if 'logtitle'        in item.keys() else None,
					bantitle        = item['bantitle']                   if 'bantitle'        in item.keys() else None,
					getfrom         = item['getfrom']                    if 'getfrom'         in item.keys() else None,
					reasons         = self.get_reasons()
				)
			)
		except KeyError: raise KeyError("Section ['removalReasons'] does not seem to exist in settings")
		return removalReasons


	"""
	Returns removal reasons as a list. Use get_reasons(local="False")
	to fetch reasons from Reddit before returning.
	"""
	@localdata
	def get_reasons(self):
		reasons = []
		try:
			for item in self.settingsJSON['removalReasons']['reasons']:
				reasons.append(
					reason(
						text           = self.__decode_text(item['text']),
						flairText      = item['flairText']      if 'flairText'      in item.keys() else None,
						flairCSS       = item['flairCSS']       if 'flairCSS'       in item.keys() else None,
						removePosts    = item['removePosts']    if 'removePosts'    in item.keys() else None,
						removeComments = item['removeComments'] if 'removeComments' in item.keys() else None,
						title          = self.__decode_text(item['title']),

					)
				)
		except KeyError: raise KeyError("Section ['removalReasons']['reasons'] does not seem to exist in settings")
		return reasons


	@localdata
	def add_reason(self, reason):
		settings = self.settingsJSON
		new_reason = {
			'text'           : self.__encode_text(reason.text),
			'flairText'      : reason.flairText,
			'flairCSS'       : reason.flairCSS,
			'removePosts'    : reason.removePosts,
			'removeComments' : reason.removeComments,
			'title'          : reason.title
		}
		settings['removalReasons']['reasons'].insert(0, new_reason)
		self.push_settings(f"\"create new rule '{reason.title}'\" via pmtw")
		return f"\"create new rule '{reason.title}'\" via pmtw"


	"""
	Returns mod macros as a list. Use get_modMacros(local="False")
	to fetch reasons from Reddit before returning.
	"""
	@localdata
	def get_modMacros(self):
		modMacros = []
		try:
			for item in self.settingsJSON['modMacros']:
				modMacros.append(
					modMacro(
						text             = self.__decode_text(item['text'])  if 'text'             in item.keys() else None,
						title            = self.__decode_text(item['title']) if 'title'            in item.keys() else None,
						distinguish      = item['distinguish']               if 'distinguish'      in item.keys() else None,
						ban              = item['ban']                       if 'ban'              in item.keys() else None,
						mute             = item['mute']                      if 'mute'             in item.keys() else None,
						remove           = item['remove']                    if 'remove'           in item.keys() else None,
						approve          = item['approve']                   if 'approve'          in item.keys() else None,
						lockthread       = item['lockthread']                if 'lockthread'       in item.keys() else None,
						lockreply        = item['lockreply']                 if 'lockreply'        in item.keys() else None,
						sticky           = item['sticky']                    if 'sticky'           in item.keys() else None,
						archivemodmail   = item['archivemodmail']            if 'archivemodmail'   in item.keys() else None,
						highlightmodmail = item['highlightmodmail']          if 'highlightmodmail' in item.keys() else None,
						contextpost      = item['contextpost']               if 'contextpost'      in item.keys() else None,
						contextcomment   = item['contextcomment']            if 'contextcomment'   in item.keys() else None,
						contextmodmail   = item['contextmodmail']            if 'contextmodmail'   in item.keys() else None
					)
				)
		except KeyError: raise KeyError("Section ['modMacros'] does not seem to exist in settings")
		return modMacros


	"""
	Returns usernote colors as a list. Use get_usernoteColors(local="False")
	to fetch reasons from Reddit before returning.
	"""
	@localdata
	def get_usernoteColors(self):
		usernote_colors = []
		try:
			for item in self.settingsJSON['usernoteColors']:
				usernote_colors.append(
					usernoteColor(
						key   = item['key']   if 'key'   in item.keys() else None,
						text  = item['text']  if 'text'  in item.keys() else None,
						color = item['color'] if 'color' in item.keys() else None
					)
				)
			return usernote_colors
		except KeyError: raise KeyError("Section ['usernoteColors'] does not seem to exist in settings")


	"""
	Returns usernote colors as a list. Use get_banMacros(local="False")
	to fetch reasons from Reddit before returning.
	"""
	@localdata
	def get_banMacros(self):
		banMacros = []
		try:
			for item in self.settingsJSON['']:
				banMacros.append(
					banMacro(
						banNote    = item['banNote']    if 'banNote'    in item.keys() else None,
						banMessage = item['banMessage'] if 'banMessage' in item.keys() else None
					)
				)
		except KeyError: raise KeyError("Section ['banMacros'] does not seem to exist in settings")
		return banMacros


