from gevent import monkey; monkey.patch_all()
from mongoengine import connect

MONGO_DB_NAME = 'trgtb-DEV'
connect(MONGO_DB_NAME)
