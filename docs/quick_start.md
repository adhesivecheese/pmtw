# Quick Start

In this section, we go over everything you need to know to start building scripts
or bots using PMTW, the Python Moderator Toolbox Wrapper.

# Prerequisites

Python Knowledge
: You need to know at least a little Python to use PMTW. PMTW supports 
[Python 3.7+](https://docs.python.org/3/tutorial/index.html). If you are stuck 
on a problem, [r/learnpython](https://reddit.com/r/learnpython) is a great place 
to ask for help.

PRAW Knowledge
: You need to have a properly configured `praw.Reddit` instance to make use of 
PMTW. Refer to [PRAW's documentation](https://praw.readthedocs.io/en/stable/getting_started/quick_start.html) for help there.

Reddit Knowledge
: A basic understanding of how Reddit works is a must. In the event you are not already familiar with Reddit start at [Reddit Help](https://www.reddithelp.com/en).

Reddit Moderator Account
: A Reddit account with permissions to access wiki pages is required to access 
and modify Toolbox's wiki pages. if using OAuth through PRAW, `wikiread` is 
required to read Toolbox's wiki pages, and `wikiwrite` to save settings or notes.

# Common Tasks

## Obtaining a `Toolbox` instance

!!! warning
	For the sake of brevity, the following examples pass authentication 
	information via arguments to `praw.Reddit()`. If you do this, you need to 
	be careful not to reveal this information to the outside world if you share 
	your code. It is recommended to use a praw.ini file in order to keep your 
	authentication information separate from your code.

A `Toolbox` instance is the recommended way of interacting with Toolbox through
PMTW. A `Toolbox` instance provides access to both Toolbox's settings and 
usernotes through `toolbox.settings` and `toolbox.usernotes` respectively.

A `Toolbox` instance is instantiated with a praw `Subreddit` instance.
For Example:

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

## Viewing Toolbox Notes on a User

With a `Toolbox` instance, a user's notes may easily be listed. For example, 
displaying notes on user `spez`:

```py
toolbox.usernotes.list_notes("spez")
```

will return a list of usernotes, from oldest to newest. To display newest notes 
first, pass the keyword argument `reverse=True` to `list_notes()`


## Creating a New Note
!!! info
	It is *highly* adviseable to pass a `praw.redditor` object for `user` argument 
	whenever practical, as that will ensure canonical capitalization of the 
 	username, as JSON keys are case-sensitive.

Creating a note is done through the creation of an instance of a 
[ToolboxNote](ToolboxNote.md) object.

For example, to create a note "Admin" on /u/spez:

```py
note = toolboxNote(reddit.Redditor("spez"), "Admin")
```

There are two ways to add your created note on Reddit. You can either pass 
a ToolboxUsernotes object in the `notes` argument:

```py
toolboxNote(reddit.Redditor("spez"), "Admin", notes=toolbox.usernotes)
```

or create the note and add it as a seperate operation:

```py
note = toolboxNote(reddit.Redditor("spez"), "Admin")
toolbox.usernotes.add(note)
```

## Removing Usernotes

!!! info
	It is *highly* adviseable to pass a `praw.redditor` object for `user` argument
	whenever practical, as that will ensure canonical capitalization of the 
 	username, as JSON keys are case-sensitive.

Removing a specific note is acomplished by calling `toolbox.usernotes.remove()` with
a username and the timestamp of the note. For example, to remove that note we 
just added on /u/spez, assuming the note's timestamp was `1665693170`:

```py
toolbox.usernotes.remove(reddit.Redditor("spez"), 1665693170)
```

Removing all notes for a given user is acomplished through the same method, 
without passing a timestamp. For example, to remove all usernotes on /u/spez:

```py
toolbox.usernotes.remove(reddit.Redditor("spez"))
```