from gevent import monkey; monkey.patch_all()
from pymongo import Connection

db = Connection()['trgtb-DEV']

from mongoengine import connect
MONGO_DB_NAME = 'trgtb-ENGINE'
connect(MONGO_DB_NAME)
print "Connected to %s" % MONGO_DB_NAME
