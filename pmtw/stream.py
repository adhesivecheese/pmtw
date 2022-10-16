import time
from typing import Any, Generator, Optional
from praw.models.util import BoundedSet, ExponentialCounter
from praw.models import ListingGenerator
from datetime import datetime

class WikiRevision:
	def __init__(self, user, timestamp, page, revision_hidden, reason, id):
		self.user = user
		self.timestamp = timestamp
		self.page = page
		self.revision_hidden = revision_hidden
		self.reason = reason
		self.id = id
		
		self.human_time = datetime.fromtimestamp(self.timestamp).__str__()

	def __repr__(self):
		return f"WikiRevision(page='{self.page}' user='{self.user}' human_time='{self.human_time}')"

def revisions_stream(
	sub=None,
	page=None,
	attribute_name: str = "id",
	pause_after: Optional[int] = None,
	skip_existing: bool = False,
	**function_kwargs: Any,
) -> Generator[Any, None, None]:
	"""
	Yield new items from a wikipage of a subreddit as they become available.

	modified from https://github.com/praw-dev/praw/blob/master/praw/models/util.py

	Parameters
	----------
	sub: praw.subreddit object
		The subreddit to stream wiki revisions from
	page: String
		the wiki page to stream from. If it's a subpage, you should pass the 
		path in the format `<folder>/<page>`
	pause_after: [Optional] Integer (Default: `None`)
		An integer representing the number of requests that result in no new 
		items before this function yields `None`, effectively introducing a 
		pause into the stream. A negative value yields `None` after items 
		from a single response have been yielded, regardless of number of new 
		items obtained in that response. A value of `0` yields `None` after 
		every response resulting in no new items, and a value of `None` never 
		introduces a pause.
	skip_existing: [Optional] Boolean (Default: False)
		When `True`, this does not yield any results from the first request 
		thereby skipping any items that existed in the stream prior to starting 
		the stream.

	additonal keyword arguments are passed to the inner function

	Yields
	------
	WikiRevision object

	Note
	----
	This function internally uses an exponential delay with jitter between 
	subsequent responses that contain no new results, up to a maximum delay of 
	just over 16 seconds. In practice, that means that the time before pause 
	for `pause_after=N+1` is approximately twice the time before pause for 
	`pause_after=N`.


	"""
	path = f'/r/{sub.display_name}/wiki/revisions/{page}'
	def function(limit=None, params=None):
		if params:
			params["before"] = "WikiRevision_" + params["before"]
		return ListingGenerator(
			reddit=sub._reddit,
			url=path,
			params=params
		)

	before_attribute = None
	exponential_counter = ExponentialCounter(max_counter=16)
	seen_attributes = BoundedSet(301)
	without_before_counter = 0
	responses_without_new = 0
	valid_pause_after = pause_after is not None
	while True:
		found = False
		newest_attribute = None
		limit = 100
		if before_attribute is None:
			limit -= without_before_counter
			without_before_counter = (without_before_counter + 1) % 30
		for item in reversed(list(function(limit=limit, **function_kwargs))):
			item = WikiRevision(
				sub._reddit.redditor(item["author"]["data"]["name"]),
				item["timestamp"],
				sub.wiki[item["page"]].revision(item["id"]),
				item["revision_hidden"],
				item["reason"],
				item["id"]
			)
			attribute = getattr(item, attribute_name)
			if attribute in seen_attributes: continue
			found = True
			seen_attributes.add(attribute)
			newest_attribute = attribute
			if not skip_existing: 
				yield item
		before_attribute = newest_attribute
		skip_existing = False
		if valid_pause_after and pause_after < 0:
			yield None
		elif found:
			exponential_counter.reset()
			responses_without_new = 0
		else:
			responses_without_new += 1
			if valid_pause_after and responses_without_new > pause_after:
				exponential_counter.reset()
				responses_without_new = 0
				yield None
			else:
				time.sleep(exponential_counter.counter())

