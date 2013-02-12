import randblog

from datetime import datetime
from time import mktime
def convert_time_tuple(t):
   return datetime.fromtimestamp(mktime(t))
