from randblog import db

item_collection = db['items']
stats_collection = db['stats']

def word_encode(word):
    return word.replace('.', '<period>').replace('$', '<dollar>')
