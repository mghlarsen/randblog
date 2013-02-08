import randblog
from randblog import db

feed_collection = db['feeds']
entry_collection = db['entries']
stats_collection = db['stats']

from datetime import datetime
from time import mktime
def convert_time_tuple(t):
   return datetime.fromtimestamp(mktime(t))
