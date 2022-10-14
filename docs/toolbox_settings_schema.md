# Toolbox Usernotes Wiki Page

Unofficial documentation. Canonnical documentation may be found
[here](https://github.com/toolbox-team/reddit-moderator-toolbox/wiki/Subreddit-Wikis%3A-toolbox).

Moderator Toolbox stores settings at `https://reddit.com/r/{sub}/wiki/toolbox`,
where `{sub}` is the name of a subreddit. The wiki is stored as a plain JSON object
with the following properties (indicated as python types after loading the JSON):

ver [Integer]
: The Settings format version. The current version of the settings page is `1`.
Increases in the version number indicate breaking changes to this schema; a
lower version of this schema should *never* be written back to the wiki.

domainTags [Empty String] or [Dictionary]
: Initially an empty string, if filled out becomes a dictionary object
keys

	name [String]
	: The domain that the tag applies to, as a string. (e.g. `"example.com"`)

	color [String]
	: The color for the tag, in CSS 6-character hex format with a leading `#`.
	(e.g. `"#0094FF"`)

removalReasons [Empty String] or [Dictionary]
: Initially an empty string, if filled out becomes a dictionary object

	pmsubject [HTML encoded String]
	: Defines the default subject to use when sending a removal reason as a 
	private message or modmail message. Accepts placeholders.

	logreason [HTML encoded String]
	: TODO

	header [HTML encoded String]
	: applied at the top of removal reason messages. Accepts placeholders.

	footer [HTML encoded String]
	: applied at the bottom of removal reason messages. Accepts placeholders.

	removalOption [String]
	: Option to suggest removal options to moderators, force options on 
	moderators, or leave up to individual moderator preference

	typeReply [String]
	: Option to leave removal message as a comment, pm, both, or send nothing 
	and log the removal

	typeStickied [Boolean]
	: If `True` and replying as a comment, sticky the comment

	typeCommentAsSubreddit [Boolean]
	: Leave removal reasons as the moderator-subreddit user

	typeLockComment [Boolean]
	: If `True` and replying as a comment, lock the comment

	typeAsSub [Boolean]
	: If `True` and replying through PM, send the PM as from the subreddit.

	autoArchive [Boolean]
	: Automatically archive sent modmail through PM (Only with new modmail)

	typeLockThread [Boolean]
	: Lock the removed thread.

	logsub [HTML encoded String]
	: A string representing a subreddit name (without the /r/) to log removal
	 reason to. Defaults to an empty string

	logtitle [HTML encoded String]
	: Title of the post made to the logsub, if logsub is set. 

	bantitle [HTML encoded String]
	: defining the default subject to use when sending a ban message.

	getfrom [String]
	: Subreddit to fetch removal reasons from. This will override all other 
	settings.

	reasons [List]
	: reasons is a list of dictionary objects. Each reason has the following
	attributes

		text [HTML encoded or unquoted String]
		: Text content of the removal reason. Accepts placeholders, as well as 
		a subset of HTML which needs to be documented. TODO

		flairText [HTML encoded String]
		: Flair text to be applied to posts this reason is used on. Empty 
		string for none.

		flairCSS [HTML encoded String]
		: Flair CSS class to be applied to posts this reason is used on. Empty 
		string for none.

		removePosts [Boolean]
		: If `True`, the removal reason is applicable to submissions.

		removeComments [Boolean]
		: If `True`, the removal reason is applicable to comments

		title [HTML encoded String]
		: Title of the removal reason.

		flairTemplateID
		: The id of a flair template to apply.


modMacros [Empty String] or [List]
: Initially an empty string, if filled out becomes a list

	text [HTML encoded String]
	: Text content of the macro reply left when the macro is used.

	title [String]
	: Title of the macro.

	distinguish [Boolean]
	: If `True`, the macro reply is distinguished when the macro is used.

	ban [Boolean]
	: If `True`, the author of the post or comment is banned when the 
	macro is used.

	mute [Boolean]
	: If `True`, the author of the post or comment is muted from modmail 
	when the macro is used.

	remove [Boolean]
	: If `True`, the post or comment is removed when the macro is used.

	approve [Boolean]
	: If `True`, the post or comment is approved when the macro is used.

	lockthread [Boolean]
	: If `True`, the thread is locked when the macro is used.

	lockreply [Boolean]
	: If `True`, the removal comment is locked when the macro is used.

	sticky [Boolean]
	: If `True`, the thread is stickied when the macro is used.

	archivemodmail [Boolean]
	: If `True`, the new modmail thread is archived when the macro is used.

	highlightmodmail [Boolean]
	: If `True`, the new modmail thread is highlighted when the macro is 
	used.

	contextpost [Boolean]
	: If `True`, macro is available for submissions

	contextcomment [Boolean]
	: If `True`, macro is available for comments

	contextmodmail [Boolean]
	: If `True`, macro is available for new modmail messages

usernoteColors [List]
: A list of dictionaries containing three keys

	key [String]
	: A string used to identify this usernote type internally. Do not change 
	this value when editing the type. Doing so will break associations to 
	existing notes.

	text [String]
	: The "title" of the note, describing what the note type represents.

	color [String]
	: Any valid CSS color string. The color associated with this note type.


banMacros [Empty String] or [Dictionary]
: Initially an empty string, if filled out becomes a dictionary object

	banNote [String]
	: The default mod-only note to save with the ban. Accepts placeholders.
	
	banMesage [String]
	: The default message sent to the user when they're banned. Accepts
	placeholders.

