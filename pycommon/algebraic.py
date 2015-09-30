# importing division from __future__ affects only this module
from __future__ import division
import collections
import operator


class AlgebraicDict(collections.MutableMapping):
    '''
    AlgebraicDict is a dict-like structure that makes it easy to manipulate
    hashtables. It supports element-wise operations like a numpy array, but is
    indexed by Python-hashable values rather than by integers.

    Presumably, the values will be numeric, but this is not required.

    A common usage is to manipulate Counter() instances. Simply call, e.g.,
    AlgebraicDict(Counter(labels)).

    All operators are interpreted in the context of importing division from
    __future__.
    '''
    def __init__(self, *args, **kwargs):
        self._dict = dict(*args, **kwargs)

    # implement the basic dict operations

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __delitem__(self, key):
        del self._dict[key]

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        return repr(self._dict)

    # add more functionality via operator overloads

    def _apply_operator(self, op_func, rhs):
        if isinstance(rhs, collections.MutableMapping):
            return AlgebraicDict({key: op_func(self[key], rhs[key]) for key in self})
        return AlgebraicDict({key: op_func(self[key], rhs) for key in self})

    def __add__(self, rhs):
        '''
        rhs can be another dict or AlgebraicDict, or a number
        '''
        return self._apply_operator(operator.add, rhs)

    def __sub__(self, rhs):
        '''
        rhs can be another dict or AlgebraicDict, or a number
        '''
        return self._apply_operator(operator.sub, rhs)

    def __mul__(self, rhs):
        '''
        rhs can be another dict or AlgebraicDict, or a number
        '''
        return self._apply_operator(operator.mul, rhs)

    def __div__(self, rhs):
        '''
        rhs can be another dict or AlgebraicDict, or a number
        '''
        return self._apply_operator(operator.truediv, rhs)

    def __truediv__(self, rhs):
        '''
        rhs can be another dict or AlgebraicDict, or a number
        '''
        return self._apply_operator(operator.truediv, rhs)

    def __pow__(self, rhs):
        '''
        rhs can be another dict or AlgebraicDict, or a number
        '''
        return self._apply_operator(operator.pow, rhs)

    def __abs__(self):
        return AlgebraicDict({key: abs(value) for key, value in self.items()})

    # and a few more useful

    def sum(self):
        '''
        Unfortunately, the Python built-in sum() does not recognize an operator
        overload like `__sum__`, so this will have to do.
        '''
        return sum(self._dict.values())

    def normalized(self):
        '''
        Returns a new AlgebraicDict `norm` such that `norm.sum() == 1`
        '''
        return self / self.sum()
