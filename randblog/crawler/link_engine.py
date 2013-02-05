from mongoengine import *

class Link(DynamicDocument):
    meta = {'collection' : 'links', 'allow_inheritance':False}
    url = StringField(required=True)
    sources = ListField(ReferenceField('CorpusItem', dbref=False))
    
    def ensure_source(self, src):
        if not src in self.sources:
            self.sources.append(src)
            return False
        return True

