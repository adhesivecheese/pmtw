# ToolboxUsernotes

A ToolboxUsernotes object Represents the Toolbox Usernotes page.

!!! note "class definition"
	```
	ToolboxUsernotes(subreddit, identifier, settingsWarnings, lazy)
	```

## Initialization Variables

### Required Arguments
subreddit
:A `praw.Reddit.subreddit` object for the subreddit to interact with usernotes with

### Optional Keyword Arguments

lazy
:A boolean value, which if set to False will prevent loading data from Reddit 
on instantiation.

identifier
:A string to identify all actions taken in the wiki save description

settingsWarnings
:A list. This keyword argument is used to ensure all configured usernote types 
are available to add to the usernotes page itself, as the usernotes wiki page 
only stores warnings which exist in the blob.

## Class Instance Variables

### warnings
Available warnings for usernotes. Includes whatever notes are already in the 
Toolbox Usernotes wiki page, as well as any additional notes passed in 
`settingsWarnings` on instantiation.

### __subreddit
A `praw.Reddit.subreddit` object for the subreddit to interact with usernotes 
with. Also used in the representation of a ToolboxUsernotes object.

### __identifier
The identifier appended to all usernote saves in the wiki edit description. 
Defaults to "via pmtw"

### __usernotesJSON
The uncompressed JSON from the usernotes wiki page, loaded as a dictionary.

### __settingsWarnings
A list of all available warnings types for a subreddit, intended to come from a 
ToolboxSettings instance.

## Class Public Methods

### save

!!! note "method definition"
	```
	save([Optional] reason:str)
	```

Saves usernotes back to reddit. Ordinarily called as part of [add](#add), but 
may be manually called if doing bulk operations. If no reason is set, the reason
on the wiki page edit description will be "Usernote update " + your identifier.

### load
!!! note "method definition"
	```
	load()
	```

Loads the content of a subreddit's usernotes wiki page into the class. If the 
usernotes page doesn't exist, calling load() will create the wiki page and 
populate it with data. The load method populates the [__usernotesJSON](#__usernotesjson)
object, as well as [warnings](#warnings)

### add
!!! note "method definition"
	```
	add(note:ToolboxNote, [Optional] lazy:bool)
	```

!!! warning
	It is *highly* adviseable to pass a `praw.redditor` object for `user` arguments
	 whenever practical, as that will ensure canonical capitalization of the 
 	username, as JSON keys are case-sensitive.

Takes a ToolboxNote object and adds it to the usernotes wiki page on Reddit.
has an optional keyword argument, `lazy`, which adds the note to the local 
copy of usernotes, but does not save to Reddit; this is useful if doing bulk 
additions.

### remove
!!! note "method definition"
	```
	remove(user:praw.redditor or str, timestamp:int, [Optional] lazy:bool)
	```

!!! warning
	PMTW will attempt to match the correct capitalization for a username if a 
	string is passed, but it is adviseable to pass a `praw.redditor` object for
	the `user` argument if practical. 

Method for removing usernotes. If a timestamp is passed when calling, PMTW will
delete the note for that user with that timestamp, if such a note exists.

If no timestamp is passed, will remove all notes for the passed user, if that 
user exists in the usernotes page.

### list_users
!!! note "method definition"
	```
	list_users([Optional] lazy:bool)
	```

Returns a list of users with notes.

If the keyword argument `lazy` is set to False, will fetch a new copy of 
usernotes from the wiki before listing.

### list_notes
!!! note "method definition"
	```
	list_notes(user:praw.redditor or str, [Optional] lazy:bool)
	```

Returns a list of notes for the specified user. Will attempt to match case if 
a string is passed for the username.

### list_all_notes
!!! note "method definition"
	```
	list_all_notes([Optional] lazy:bool, [Optional] reverse:bool)
	```

Returns a list of all notes stored in the usernotes wiki, in chronological order.

If the keyword argument `lazy` is set to False, will fetch notes from the wiki 
before listing. 

If the keyword argument `reverse` is set to True, the returned list will be in 
reverse-chronological order.

### stream
!!! note "method definition"
	```
	stream([Optional] pause_after:int, [Optional] skip_existing:bool)
	```

Yields new [WikiRevision] objects for the usernotes page.

pause_after
: An integer representing the number of requests that result in no new items 
before this function yields `None`, effectively introducing a pause into the 
stream. A negative value yields `None` after items from a single response have 
been yielded, regardless of number of new items obtained in that response. A 
value of `0` yields `None` after every response resulting in no new items, and 
a value of `None` never introduces a pause.

skip_existing
: When `True`, this does not yield any results from the first request thereby 
skipping any items that existed in the stream prior to starting the stream.

## Class Private Methods

### __expand_json
!!! note "method definition"
	```
	__expand_json(notes:dict)
	```

Expands the blob portion of usernotes. The resulting dictionary is saved in 
[__usernotesJSON](#usernotesjson), as well as returning the dictionary.

### __compress_json
!!! note "method definition"
	```
	__compress_json([Optional] notes:dict)
	```

Compresses the usernotes portion back into a blob for saving in the usernotes 
wiki page, and returns the modified dictionary as a string.

### __get_warnings
!!! note "method definition"
	```
	__get_warnings()
	```

sets the [warnings](#warnings) instance variable from warnings found in the 
usernotes wiki page, as well as any additonal note types passed in 	through 
[__settingsWarnings](#__settingswarnings).

### __get_mod_index
!!! note "method definition"
	```
	__get_mod_index(self, mod:str)
	```

Returns the integer index in the users portion of the usernotes json for the 
given mod. If the mod doesn't currently exist in the wiki, adds the mod before 
returning the index.

### __get_warning_index
!!! note "method definition"
	```
	__get_warning_index(self, mod:str)
	```

Returns the integer index in the warnings portion of the usernotes json for the 
given warning. If the warning doesn't currently exist in the wiki but is a valid 
note type (per [warnings](#warnings)) adds the warning before returning the index.
returning the index.

### __match_username
!!! note "method definition"
	```
	__match_username(self, username:str)
	```

Attempts to match the capitalization for a user with an existing user already in
the wiki. If no results are found, returns the username as is, otherwise returns 
the canonnical capitalization.