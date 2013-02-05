from randblog.rss.feed_engine import Feed
from mongoengine import *

class Entry(DynamicDocument):
    feed = ReferenceField('Feed', dbref=False, required=True)
    entry_id = StringField(required=True) #This is the ID in the RSS feed
    title = StringField(required=True)
    corpus_item = ReferenceField('CorpusItem', dbref=False)
    links = ListField(ReferenceField('Link', dbref=False))
    author = StringField()
    published = DateTimeField()
    updated = DateTimeField()

