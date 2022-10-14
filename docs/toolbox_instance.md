# The Toolbox Instance

## Creating an Instance

!!! note "class definition"
	```
	Toolbox(subreddit, lazy=False, identifier=DEFAULT_IDENTIFIER))
	```

The Toolbox class provides convenient access to Toolbox's settings and usernotes.
The Canonical way to obtain an instance of this class is via:

```py
import praw
import pmtw

reddit = praw.Reddit(
    client_id="my client id",
    client_secret="my client secret",
    password="my password",
    user_agent="my user agent",
    username="my username",
)

toolbox = pmtw.Toolbox(
	reddit.subreddit("my moderated subreddit")
)
```

The only required argument is:
subreddit
: a `praw.subreddit` object for the subreddit you wish to use the Toolbox object with


Two additional keyword arguments exist for a Toolbox instance:

lazy
: a Boolean. If set to False, will not load settings and usernotes on creation
of an instance Whether to fetch settings and usernotes on instantiation

identifier
: By default, PMTW appends `via pmtw` to all descriptions for a wiki page edit. 
This identifier can be changed by passing the keyword argument `identifier` as 
part of instantiating a Toolbox object.

Toolbox's identifier may be set to anything you'd like. For example, to set 
the identifier to `my modbot`:

```py
toolbox = pmtw.Toolbox(
	reddit.Subreddit("my moderated subreddit"),
	identifier="via modbot"
)
```
### Class Instance Variables

### [usernotes](ToolboxUsernotes.md)
an instance of [ToolboxUsernotes](ToolboxUsernotes.md) for the Toolbox object's 
subreddit

### [settings](ToolboxSettings.md)
an instance of [ToolboxSettings](ToolboxSettings.md) for the Toolbox object's 
subreddit

### identifier
The ending portion of a description on a wikiedit.

### __subreddit
the `praw.Reddit.subreddit` object passed to Toolbox on instantiation. Passed 
to settings and usernotes.

## Class Methods

### prune_notes
!!! note "method definition"
	```
	prune_notes([Optional]days:int, [Optional] before:int, [Optional] excludeKinds:list, [Optional] dryRun:bool)
	```
Bulk-removes old usernotes. By default, removes all notes older than 180 days.

All arguments for prune_notes are keyword arguments:

days
: number of days to prune notes back. Ignored if `before` is set.

before
: unix timestamp (in seconds) to remove notes before

excludeKinds
: List, String list of usernote warning types to preserve, even if older than 
the specified cutoff

dryRun
: BoolSimulates removal of notes without actually affecting them.
		
prune_notes returns a string that notifies you of how many usernotes were deleted.

### search_notes
!!! note "method definition"
	```
	search_notes(query:str, [Optional] kind:str, [Optional] range:str, [Optional] lazy:bool)
	```

Search usernotes. 

query
: A required argument. the text you wish to search. not used if searching by time.

kind
: What to search. options are: `note`, `user`, `mod`, `warning`, `url`, `time`

range
: if doing a time based search, range is whether you wish to search `before` or
`after` the specified timeframe

lazy
: if set to False, will reload usernotes before performing search.


### export_notes
!!! note "class definition"
	```
	export_notes([Optional file:str, [Optional] fields:list, [Optional] sortKey:str)
	```

Exports notes to a CSV file.

file
: is the name of the file to export to; this defaults to 
`usernotes-<subreddit>-<current unix timestamp in seconds>`.

fields
: A list of fields in the usernote you wish to export. Defaults to all fields in
a usernote, in the order that they appear in a [ToolboxUsernote](ToolboxNote.md)
instance. You can pass a list with fewer fields, or in a different order, to 
customize your export.

sortKey
: A string, the key in fields you wish to sort your export by. Defaults to time.


### _load
!!! note "method definition"
	```
	load()
	```

`_load()` may be called at any time to reload settings and usernotes 
from Reddit. Generally you don't want to do this, instead using 
`usernotes.load()` or `settings.load()` to not reload 
unnessesary data.
