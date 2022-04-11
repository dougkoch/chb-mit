import os
from functools import wraps

def cached_getter(func):
    @wraps(func)
    def wrapped(self,*args,**kwargs):
        if not hasattr(self,f"_{func.__name__}_cache") \
            or getattr(self,f"_{func.__name__}_cache") is None:
            setattr(self,f"_{func.__name__}_cache",func(self,*args,**kwargs))
        return getattr(self,f"_{func.__name__}_cache")
    return wrapped

def download_data(basedir):
    os.system(f'cd {basedir} && wget -r --no-parent https://physionet.org/pn6/chbmit')