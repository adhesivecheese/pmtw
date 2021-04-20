import praw
import pmtw
import csv
from datetime import datetime

r = praw.Reddit("<praw config>")
sub = r.subreddit("<subreddit>")

notes = pmtw.Usernotes(r, sub)
settings = pmtw.Settings(r, sub)

def display_usernotes(user, timestamp=True):
	users_notes = notes.get_user_notes(user)
	note_list = [f"Notes for {user}"]
	for note in users_notes:
		if timestamp: note_list.append(f"{note.warning}: '{note.note}' | {datetime.fromtimestamp(note.time)}")
		else: note_list.append(f"{note.warning}: '{note.note}' | {note.time}")
	return note_list


def export_usernotes(usernotes, file="usernotes.csv", fields=["user", "note", "time", "mod", "warning", "link", "subreddit"], sortKey="time"):
	rows = []
	for username in usernotes.existing_users():
		users_notes = usernotes.get_user_notes(username)
		for note in users_notes:
			row = []
			for field in fields: row.append(eval(f"note.{field}"))
			rows.append(row)
	try:
		rows = sorted(rows, key = lambda x: x[fields.index(sortKey)])
	except:
		rows = sorted(rows, key = lambda x: x[0])
	csv_dump = open(file, 'w')
	csv_writer = csv.writer(csv_dump)
	csv_writer.writerow(fields)
	for row in rows: csv_writer.writerow(row)
	csv_dump.close()
	return f"Usernotes exported to {file}"
