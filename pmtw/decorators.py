import functools


def batch(func):
    """
    If batch="True", prevent fetching JSON from Reddit before a function and pushing JSON back to Reddit as result.
    Useful for batch modifying usernotes.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        batchmode = kwargs.get('batch', False)
        kwargs.pop('batch', None)
        if batchmode == False:
            self._Usernotes__fetch_from_reddit()
        ret = func(self, *args, **kwargs)
        if batchmode == False:
            self.push_usernotes(ret)
        return ret
    return wrapper


def localdata(func):
    """
    Run on the locally cached JSON by default.
    Pass local="False" to fetch notes from
    Reddit before execution.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        classname = str(func.__qualname__).split('.')[0]
        local_data = kwargs.get('local', True)
        kwargs.pop('local', None)
        if classname == "Usernotes":
            if local_data == False:
                self._Usernotes__fetch_from_reddit()
        elif classname == "Settings":
            if local_data == False:
                self._Settings__fetch_from_reddit()
        return func(self, *args, **kwargs)
    return wrapper
