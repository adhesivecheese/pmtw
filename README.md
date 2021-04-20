PMTW
===

Python Moderator Toolbox Wrapper.

Built to interact with Moderator Toolbox's usernotes and settings.
Toolbox's usernotes spec may be found [here](https://github.com/toolbox-team/reddit-moderator-toolbox/wiki/Subreddit-Wikis%3A-usernotes), and the settings spec may be found [here](https://github.com/toolbox-team/reddit-moderator-toolbox/wiki/Subreddit-Wikis%3A-toolbox).

## Requirements
* [PRAW](https://github.com/praw-dev/praw) (tested on version 6.5)
* Python >3.6

## Notes
* PMTW only supports usernotes schema version 6 and settings schema version 1.
* PMTW is very much still in alpha. You can read coverage status [here](https://github.com/adhesivecheese/pmtw/wiki/Status).

## Documentation

Documentation will eventually live on a wiki page. For now, the code is (I hope) reasonably well documented and should be fairly useful, especially when combined with the following examples.

## Examples

*Setup code, needed for all following examples*

```python
import praw
import pmtw

r = praw.Reddit(<praw_config>)
sub = r.subreddit('<subreddit>')
notes = pmtw.Usernotes(r, sub)
settings = pmtw.Settings(r, sub)
```

*Reading a user's notes*

```python
from datetime import datetime
user = "adhesivecheese" #note that the capitalization doesn't matter
users_notes = notes.get_user_notes(user)
note_list = [f"Notes for {user}"]
for note in users_notes:
	note_list.append(f"{note.warning}: '{note.note}' - {datetime.fromtimestamp(note.time)}")
for note in note_list:
    print(note)
```

*Reading the individual removal reasons*

```python
reasons = settings.get_reasons()
for reason in reasons:
    print(reason.title)
    print(reason.text)
```

*Adding a note*

```python
# Create given note with time set to current time
link = 'http://www.reddit.com/abcdef'
n = pmtw.Note(user='username', note='note', link=link, warning='permban')
un.add_note(n)
```

*exporting usernotes to a csv file*

```python
import csv

def export_usernotes(
                        usernotes,
                        file="usernotes.csv",
                        fields=["user", "note", "time", "mod", "warning","link", "subreddit"],
                        sortKey="time"
                    ):
	rows = []
	for username in notes.existing_users():
		users_notes = notes.get_user_notes(username)
		for x in users_notes:
			row = []
			for field in fields: row.append(eval(f"x.{field}"))
			rows.append(row)
	try: rows = sorted(rows, key = lambda x: x[fields.index(sortKey)])
	except: rows = sorted(rows, key = lambda x: x[0])
	csv_dump = open(file, 'w')
	csv_writer = csv.writer(csv_dump)
	csv_writer.writerow(fields)
	for row in rows: csv_writer.writerow(row)
	csv_dump.close()
	return f"Usernotes exported to {file}"
	
print(notes.export_usernotes(fields=["user", "note", "time"], sortKey="link"))
```

*Pruning notes older than 365 days*

```python
import time

days_to_keep = 365
oldest_note_to_keep = int(time.time()) - (86400 * days_to_keep)
prunecount = 0
for user in notes.existing_users():
    for note in notes.get_user_notes(user):
        if note.time < oldest_note_to_keep:
            # Batch="True" prevents every single deletion from triggering a usernotes update
            notes.remove_note(user, note.time, batch="True") 
            prunecount +=1
            
# Now update the usernotes on Reddit
notes.push_usernotes(f"pruned {prunecount:,} notes older than 365 days with pmtw")
```

## Thanks

PMTW owes a great deal to the existance of danthedaniel's excelent [PUNI](https://github.com/danthedaniel/puni). While not exactly a fork, it does borrow much in structure from PUNI; just better suited and expanded to my individual needs.
