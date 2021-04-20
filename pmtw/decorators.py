import functools

"""
By passing batch="True", prevent fetching JSON from
Reddit before a function and pushing JSON back to Reddit
as result. Useful for batch modifying usernotes.
"""
def batch(func):
	@functools.wraps(func)
	def wrapper(self, *args, **kwargs):
		batchmode = kwargs.get('batch', False)
		kwargs.pop('batch', None)
		if batchmode == False: self._Usernotes__fetch_from_reddit()
		ret = func(self, *args, **kwargs)
		if batchmode == False: self.push_usernotes(ret)
		return ret
	return wrapper

"""
Run on the locally cached JSON by default.
Pass local="False" to fetch notes from
Reddit before execution.
"""
def localdata(func):
	@functools.wraps(func)
	def wrapper(self, *args, **kwargs):
		className = str(func.__qualname__).split('.')[0]
		localdata = kwargs.get('local', True)
		kwargs.pop('local', None)
		if className == "Usernotes":
			if localdata == False: self._Usernotes__fetch_from_reddit()
		elif className == "Settings":
			if localdata == False: self._Settings__fetch_from_reddit()
		ret = func(self, *args, **kwargs)
		return ret
	return wrapper
