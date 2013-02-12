def word_encode(word):
    return word.replace('.', '<period>').replace('$', '<dollar>')
