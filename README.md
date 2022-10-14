# Installation

PMTW requires Python 3.7+. The recommended way to install PMTW is via [pip](https://pypi.python.org/pypi/pip)

```bash
pip install pmtw
```

For instructions on installing Python and pip see "The Hitchhiker's Guide to Python"
[Installation Guides](https://docs.python-guide.org/en/latest/starting/installation/)

# Quickstart

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

Once you have a `toolbox` instance, you can interact with usernotes through
`toolbox.usernotes` and settings through `toolbox.settings`

# Documentation

PMTW's documentation is located at https://pmtw.readthedocs.io/

# License

PMTW's source is provided under the [Simplified BSD License](https://github.com/praw-dev/praw/blob/0860c11a9309c80621c267af7caeb6a993933744/LICENSE.txt)

- Copyright ©, 2021, 2022 adhesiveCheese