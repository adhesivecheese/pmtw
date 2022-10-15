# ToolboxNote

!!! note "class definition"
	```
	ToolboxNote(user, note, [Optional]warning:str, [Optional]time:int, [Optional]mod:str, [Optional]url:str, [Optional]link:str, [Optional]notes:ToolboxUsernotes)
	```
## Initialization Variables

### Required Arguments

user
: Required as the first positional argument. The user to leave the note for.
Accepts a string or a `praw.redditor` object. As usernotes are assigned in a 
case-sensitive manner, it is adviseable to pass a `praw.redditor` object 
whenever possible to get the canonical capitalization of the username.

note
: Required as the second positional argument. Takes a string as the note 
intended to be left for the user.

### Optional Keyword Arguments

warning
: Keyword argument, optional, string. Defaults to `None`. This must be either
`None` or an already-configured note type. (Available note types may be found by
 checking `toolbox.usernotes.warnings`). Adding a note with an invalid warning 
 kind will raise a ValueError.

time
: Keyword argument, optional, integer. A Unix timestamp in seconds. If a time 
is not explicitly passed, the note's time will be set to the current time.

mod
: Keyword argument, optional, string. The moderator issuing the note. If not
specified, when added to the wiki the mod will be set to the username of the 
praw user running PMTW.

url
: Keyword argument, optional, string. A URL for the note. Defaults to `None`. 
Accepts most variations of valid reddit URLs, and will be used to set the link
value if not otherwise specified, as toolbox compresses many kinds of links.

link
: A toolbox-formatted url as a string. The link as will be saved to the Toolbox
usernotes blob. Reddit links other than modmail are generally compressed; 
unless you know for sure what you're doing it's best to leave this unset.

notes
: [`ToolboxUsernotes`](ToolboxUsernotes.md) object. Defaults to `None`. If 
set, will instantly add the note on Reddit.

A ToolboxUsernote has one additional convenience attribute: `human_time`, which 
will convert the timestamp to a human-readable format.


## Accepted URL formats

ToolboxNote will compress many forms of Reddit links.

protocol (may be ommitted)
: `http://`,`https://`

subdomain (may be ommitted)
: `www`, `old`, `new`, or any other three-letter subdomain. 

domain
: `reddit.com`, `redd.it`

path
: most any variation on a path; either just the id, the full url, or anything
in-between

### examples
* `https://www.reddit.com/r/subreddit/abcdef/comments/ghijkl/`
* `http://old.reddit.com/r/subreddit/abcdef/`
* `http://reddit.com/r/subreddit/abcdef`
* `http://reddit.com/abcdef`
* `https://redd.it/abcdef`
* `reddit.com/abcdef`

## Class Private Methods

### __expand_link
!!! note "method definition"
	```
	@staticmethod
	__expand_link(link:str)
	```
	expands a Toolbox formatted shortlink to a valid url.

### __compress_link
!!! note "method definition"
	```
	@staticmethod
	__compress_link(url:str)
	```
	Attempts to compress the provided url to a Toolbox Formatted shortlink. Does
	**not** compress message links.

