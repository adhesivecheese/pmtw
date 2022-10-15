# PMTW: The Python Moderator Toolbox Wrapper

PMTW is a series of utilities built using PRAW to interact with 
[Moderator Toolbox](https://github.com/toolbox-team/reddit-moderator-toolbox) 
usernotes and settings. It can serve as a near drop-in replacement for 
[PUNI](https://github.com/danthedaniel/puni), requiring only import modifications.

PMTW requires [PRAW](https://github.com/praw-dev/praw).

PMTW operates on Toolbox Settings version 1, and Usernotes version 6.

PMTW's documentation is organized into the following sections:

* [Getting Started](#getting-started)
* [Code Overview](#code-overview)
* [Tutorials](#tutorials)
* [Package Info](#package-info)
* [Toolbox Schema Information](#toolbox-schema-information)

# Document Conventions

Unless otherwise noted, all examples in this document assume `subreddit` is a
PRAW `subreddit()` object.

# Getting Started

* [Quick Start](quick_start.md)
* [Installing PMTW](installing.md)

# Code Overview

* [The Toolbox Instance](toolbox_instance.md)
* [ToolboxUsernotes](ToolboxUsernotes.md)
* [ToolboxSettings](ToolboxSettings.md)
* [ToolboxNote](ToolboxNote.md)
* [Other Classes](other_classes.md)

# Package Info

* [Change Log](changelog.md)
* [Contributing](contributing.md)
* [References](references.md)

# Toolbox Schema Information

* [Usernotes](toolbox_usernote_schema.md)
* [Settings](toolbox_settings_schema.md)