from gevent import monkey; monkey.patch_all()
from pymongo import Connection

db = Connection()['trgtb-DEV']
