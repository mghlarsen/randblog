from randblog import db
from urlparse import urlsplit, SplitResult
import re

__all__ = ['clean_link', 'link_collection']

__utm_matcher = re.compile(r'((?:\?|\&)utm_[_a-z]+=[^&]*)(?:\Z|\&)')

def clean_link(url):
    o = urlsplit(url)
    if o.query and __utm_matcher.match(o.query):
        query = __utm_matcher.sub('', o.query)
        return SplitResult(o.scheme, o.netloc, o.path, query, fragment).geturl()
    else:
        return o.geturl()

link_collection = db['links']

