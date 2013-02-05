from mongoengine import *

class CorpusItemSource(EmbeddedDocument):
    type = StringField(required=True)
    rss_feed_id = ReferenceField('Feed', dbref=False)
    rss_feed_name = StringField()
    rss_feed_entry_id = ReferenceField('Entry', dbref=False)
    rss_feed_entry = StringField()

class CorpusItemLink(EmbeddedDocument):
    href = StringField(required=True)
    title = StringField(required=True)
    id = ReferenceField('Link', dbref=False)

class CorpusItem(DynamicDocument):
    meta = {'collection' : 'items', 'allow_inheritance':False}
    updated = DateTimeField()
    title = StringField()
    text = StringField()
    source = EmbeddedDocumentField(CorpusItemSource, required=True)
    links = ListField(EmbeddedDocumentField(CorpusItemLink))
    
    def get_split_words(self):
        words = self.text.split()
        while len(words) > 0 and words[-1] == '|':
            words.pop()
        return words

    def extract_crawl_links(self):
        updated = 0
        link_updated = 0
        existing = 0
        need_save = False
        for link in self.links:
            pass
