import csv
import time as t

from pmtw.constants import DEFAULT_IDENTIFIER
from pmtw.settings import ToolboxSettings
from pmtw.usernotes import ToolboxUsernotes


class Toolbox:
	def __init__(self, subreddit, lazy=False, identifier=DEFAULT_IDENTIFIER):
		"""
		Constructor for the Toolbox class

		Parameters
		----------
		subreddit: praw.subreddit object
			the subreddit to use the Toolbox object with
		lazy: Bool
			Whether to fetch settings and usernotes on instantiation
		identifier: String
			string that get's appended to all wikiedit discriptions identifying
			pmtw as the actioner. Defaults to "via pmtw"
		"""
		self.settings = ''
		self.usernotes = ''
		self.identifier = identifier
		self.__subreddit = subreddit
		if not lazy: self._load()
			
	def __repr__(self):
		"""Set display for a Toolbox object"""
		return f"Toolbox(subreddit='{self.__subreddit}')"

	def _load(self):
		"""Load settings and Usernotes"""
		self.settings = ToolboxSettings(self.__subreddit, identifier=self.identifier)
		self.usernotes = ToolboxUsernotes(self.__subreddit, identifier=self.identifier, settingsWarnings=self.settings.warnings)

	def prune_notes(self, days=180, before=None, excludeKinds=[], dryRun=False):
		"""
		Bulk-removes old usernotes.

		Parameters
		----------
		days: Int
			number of days to prune notes back. Ignored if before is set.
		before: Int
			unix timestamp (in seconds) to remove notes before
		excludeKinds: List, String
			list of usernote warning types to preserve, even if older than the
			specified cutoff
		dryRun: Bool
			Simulates removal of notes without actually affecting them.
		
		Returns
		-------
		string
			notification of how many usernotes were deleted.

		"""
		self.usernotes.load()
		if isinstance(excludeKinds, str): excludeKinds = [excludeKinds]
		if before: pruneTime = before
		else: pruneTime = t.time() - (days * 86400)
		users_count = 0
		notes_count = 0
		preserved_count = 0
		for user in self.usernotes.list_users():
			users_notes = self.usernotes.list_notes(user)
			user_triggered = False
			for note in users_notes:
				if note.time > pruneTime: continue
				if note.warning in excludeKinds:
					preserved_count +=1
					continue
				notes_count += 1
				user_triggered = True
				self.remove(user, note.time, bulk_action=True)
			if user_triggered == True: users_count += 1
		if dryRun:
			self.usernotes.load()
			return f"prune would bulk delete {notes_count:,} notes on {users_count:,} users older than {days} days."
		else:
			self.usernotes.save(f"bulk deleted {notes_count:,} notes on {users_count:,} users older than {days} days")
			return f"bulk deleted {notes_count:,} notes on {users_count:,} users older than {days} days"

	def search_notes(self, query, kind="note", range="after", lazy=True):
		"""
		Search usernotes. 

		Parameters
		----------
		query: String
			the parameter to be searched
		kind: String
			one of: note, user, mod, warning, url, time
		range: String
			one of: before, after
		lazy: Bool
			if True, fetch from Reddit before searching

		Returns
		-------
		List
			a list of ToolboxUsernote objects matching the query parameter, or
			an empty list if there are no matches

		Raises
		------
		ValueError
			* when range is invalid if kind="time"
			* when kind is invalid
		"""
		if not lazy: self.usernotes.load()
		notes = self.usernotes.list_all_notes()
		results = []

		for note in notes:
			if kind == "time":
				if range == "after" and note.time > int(query): results.append(note)
				if range == "before" and note.time < int(query): results.append(note)
				else: raise ValueError(f"{range} is invalid. range options are ['before', 'after']")

			if kind == "note": search = note.note
			elif kind == "user": search = note.user
			elif kind == "mod": search = note.mod
			elif kind == "warning": search = note.warning
			elif kind == "url": search = note.url
			else: raise ValueError(f"{kind} is not a valid search option")

			search = str(search)
			search = search.lower()
			if query.lower() in search: results.append(note)
		return results

	def export_notes(
		self, 
		file="",
		fields=["user","note","warning","time","mod","link"],
		sortKey="time"
	):
		"""
		Exports Usernotes in a CSV file.

		Parameters
		----------
		file: String
			File name for the exported notes. Defaults to 
			"usernotes-{subreddit}-{current timestamp in seconds}.csv"
		fields: List:
			List of fields to export. Defaults to all fields
		sortKey: String
			Which key in fields to sort usernotes for in the exported csv file.
			defaults to time.

		Returns
		-------
		String
			Notification of success

		"""
		if file == "": file = f"usernotes-{self.__subreddit}-{int(t.time())}.csv"
		rows = []
		count = 0
		for note in self.usernotes.list_all_notes():
			row = []
			count += 1
			for field in fields: row.append(eval(f"note.{field}"))
			rows.append(row)
		try: rows = sorted(rows, key = lambda x: x[fields.index(sortKey)])
		except: rows = sorted(rows, key = lambda x: x[0])
		csv_dump = open(file, 'w')
		csv_writer = csv.writer(csv_dump)
		csv_writer.writerow(fields)
		for row in rows: csv_writer.writerow(row)
		csv_dump.close()
		return f"{count:,} usernotes exported to {file}"
