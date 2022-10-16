
# ToolboxSettings

A ToolboxUsernotes object Represents the Toolbox Settings page.

!!! note "class definition"
	```
	ToolboxSettings(subreddit, identifier, lazy)
	```

## Initialization Variables

### Required Arguments
subreddit
:A `praw.Reddit.subreddit` object for the subreddit to interact with usernotes with

### Optional Keyword Arguments

lazy
: A boolean value, which if set to False will prevent loading data from Reddit 
on instantiation.

identifier
: A string to identify all actions taken in the wiki save description

## Class Instance Variables
identifier: String
: A string to identify all actions taken in the wiki save description

ver: Integer
: The version of the Toolbox Settings page

domainTags
: TODO

removalReasons
: TODO

modMacros
: TODO

usernoteColors
: TODO

banMacros
: TODO

warnings: [List]
: extracted list of `key` values from usernoteColors 

__subreddit
: A `praw.Reddit.subreddit` object for the subreddit to interact with settings 
with.

__settings
: TODO

## Class Public Methods

### load

### save

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