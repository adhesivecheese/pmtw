# Compatibility Wrappers

Compatibility wrappers are provided as a courtesy; current PMTW functionality 
will not be altered to provide better compatibility if there are discrepencies.

## PMTW 0.2.x

PMTW offers the classes [Note](#note), [Usernotes](#usernotes), and 
[Settings](#settings) to provide drop-in compatibility for users who wrote 
scripts on PMTW version 0.2.1 or earlier. These classes largely just call the 
1.x classes, but provide the expected returns from this version... including
quirks like printing the url when adding a note. As 0.2.x was severely 
under-documented, time will not be devoted to thouroughly documenting every
instance variable and class method.

### Note
!!! note "class definition"
	```
	Note(user:str, note:str, [Optional] time:int, [Optional] mod:str, [Optional] warning:str, [Optional] link:str, [Optional]subreddit:str)
	```

Notes of this class will expand toolbox shortlinks as a Reddit shortlink in the 
`https://redd.it/abcdef` format.

### Usernotes
!!! note "class definition"
	```
	Usernotes(r:praw.reddit object, sub:praw.reddit.subreddit object, fetch:bool)
	```
r is actually unused in this reimplementation wrapper, as the reddit instance 
is pulled from the subreddit instance.

### Settings
!!! note "class definition"
	```
	Settings(r:praw.reddit object, sub:praw.reddit.subreddit object, fetch:bool)
	```
r is actually unused in this reimplementation wrapper, as the reddit instance 
is pulled from the subreddit instance.

The only known difference to be aware of is cosmetic - when deleting a usernote with 
PMTW 0.2.x, the wiki description would give the timestamp in milliseconds; as 
the remove_note is a wrapper for [ToolboxUsernotes.remove](ToolboxUsernotes.md#remove),
the timestamp is reported in seconds.

## PUNI

PMTW offers the classes puni_Note, puni_UserNotes to provide near-drop-in 
compatibility for users who wrote scripts using PUNI. If you have a script which
relies on PUNI you don't wish to rewrite, changing your import statements from
`from puni import Note` to `from pmtw import puni_Note as Note` and 
`from puni import UserNotes` to `from pmtw import puni_UserNotes as UserNotes` 
should provide the functionality you expect from puni, with the ability to use
your scripts with current versions of praw.

remove_note will report a ToolboxUsernotes style removal message for the wiki
edit description, but will return the string that you would expect from puni.

Further documentation for puni may be found [here](https://github.com/danthedaniel/puni/wiki/Documentation)