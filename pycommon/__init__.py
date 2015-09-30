from __future__ import division
import itertools
import operator
import pkg_resources

__version__ = pkg_resources.get_distribution('python-common').version


get0 = operator.itemgetter(0)
get1 = operator.itemgetter(1)


def jaccard(A, B):
    '''
    Return the Jaccard similarity (the size of the intersection divided by the
    size of the union) between two sets.

    This function converts each argument to a set before performing the
    computation.
    '''
    A_set = set(A)
    B_set = set(B)
    return len(A_set & B_set) / len(A_set | B_set)


def head(iterable, n=10):
    '''
    Take the first `n` entries from `iterable` and return them as a list.
    '''
    return list(itertools.islice(iterable, n))


def product(xs):
    '''
    Compute the product of all values in `xs`. Returns 1 if `xs` is empty.
    '''
    #return math.exp(sum(math.log(x) for x in xs))
    return reduce(operator.mul, xs, 1)


def pick(mapping, keys):
    '''
    Return a new dict that's identical to `mapping` but includes only the
    key-value pairs that have a key in `keys`.
    '''
    keyset = set(keys)
    return {key: value for key, value in mapping.items() if key in keyset}


def omit(mapping, keys):
    '''
    Return a new dict that's identical to `mapping` but excludes any key-value
    pairs that have a key in `keys`.
    '''
    keyset = set(keys)
    return {key: value for key, value in mapping.items() if key not in keyset}


def invert(mapping):
    '''
    Return a new dict that maps from the values of `mapping` to their original
    keys.
    '''
    return {value: key for key, value in mapping.items()}


def select(indexable, indices):
    '''
    Pick the items from indexable with the indices in `indices`.
    Useful when you want to use something like numpy's indexing feature without
    using numpy's arrays.
    '''
    return [indexable[index] for index in indices]


def uniq(iterable, keyfunc=None):
    '''
    Iterate over the consecutively unique values in iterable. This works more
    like the POSIX `uniq` rather than Python's `set()` coercion, since it may
    contain duplicate values, but it guarantees that any two consecutive values
    will be distinct.
    '''
    for value, _ in itertools.groupby(iterable, keyfunc):
        yield value


def uniq_c(iterable, keyfunc=None):
    '''
    Like uniq, but yields tuples of (value, count), kind of like POSIX `uniq -c`
    '''
    for value, values in itertools.groupby(iterable, keyfunc):
        yield value, len(list(values))


def groupby_select(iterable, keyfunc, valfunc):
    '''
    Like the standard itertools.groupby, but maps the subiterators through
    valfunc.
    '''
    for key, sub_iterator in itertools.groupby(iterable, keyfunc):
        yield key, (valfunc(sub_item) for sub_item in sub_iterator)
