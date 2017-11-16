import re
import codecs
import os.path

from .memo import memoized_property


class TextFile(object):
    '''
    TextFile is a representation of a text file on disk that memoizes (caches)
    most of its functionality.

    TODO: abstract the tokenizer somehow
    '''
    def __init__(self, filepath, encoding='utf-8'):
        self.filepath = filepath
        self.encoding = encoding

    @memoized_property
    def filename(self):
        return os.path.basename(self.filepath)

    @memoized_property
    def exists(self):
        return os.path.exists(self.filepath)

    @memoized_property
    def string(self):
        return codecs.open(self.filepath, encoding=self.encoding).read()

    @memoized_property
    def tokens(self):
        return re.findall(r'[-0-9A-Za-z_]+', self.string)

    @memoized_property
    def token_set(self):
        return set(self.tokens)

    def __repr__(self):
        return '<TextFile({filepath})>'.format(filepath=self.filepath)


_whitespace_chars = ['\t', '\n', '\x0b', '\x0c', '\r']  # ordinals: [9, 10, 11, 12, 13]
_whitespace_mapping = str.maketrans({ord(char): ' ' for char in _whitespace_chars})


def normalize_whitespace(dirty_string):
    '''
    Replace all unusual whitespace in dirty_string with
    '''
    return dirty_string.translate(_whitespace_mapping)


default_stopwords = frozenset({'and', 'of', 'in', 'the', 'for', 'a', 'on', 'to', 'with', 'an'})


def tokenize(string, stopwords=default_stopwords):
    '''
    Lowercase string, then find all word fragments in it,
    where a word fragment is designated by r'\\b\\w+\\b'.
    '''
    return [token for token in re.findall(r'\b\w+\b', string.lower()) if token not in stopwords]
