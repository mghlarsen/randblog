from randblog.rss.feed_engine import Feed
from mongoengine import *

class Entry(DynamicDocument):
    meta = {'collection' : 'entries', 'allow_inheritance':False}
    feed = ReferenceField('Feed', False) #FIXME
    feed_name = StringField()
#    corpus_item = ReferenceField('CorpusItem') #FIXME
#    links = ListField(ReferenceField('Link')) #FIXME
    author = StringField()
    published = DateTimeField()
    updated = DateTimeField()

