from gevent import monkey; monkey.patch_all()
from pymongo import Connection
from mongoengine import connect

MONGO_DB_NAME = 'trgtb-DEV'
connect(MONGO_DB_NAME)

db = Connection()[MONGO_DB_NAME]
