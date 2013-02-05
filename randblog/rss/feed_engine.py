from mongoengine import *

class FeedCleanAction(EmbeddedDocument):
    meta = {'allow_inheritance':False}
    task = StringField(required=True)
    selector = StringField(required=True)
    contains_text = StringField()

class FeedStatus(DynamicEmbeddedDocument):
    meta = {'allow_inheritance':False}
    updated = DateTimeField()
    etag = StringField()
    modified = DateTimeField()
    version = StringField()
    encoding = StringField()
    

class Feed(DynamicDocument):
    meta = {'collection' : 'feeds', 'allow_inheritance':False}
    name = StringField(required=True)
    url = StringField(required=True)
    title = StringField()
    subtitle = StringField()
    link = StringField()
    status = EmbeddedDocumentField(FeedStatus)
    clean_actions = ListField(EmbeddedDocumentField(FeedCleanAction))

