def memoized_property(getter_function):
    '''
    This can be used in place of @property. It works much the same way,
    but caches the result of the @property call in self.__{propname}, where
    {propname} is the value of the getter_function.func_name attribute.

    Use like:

        from pycommon.memo import memoized_property

        class TextFile:
            def __init__(self, filepath):
                self.filepath = filepath

            @memoized_property
            def text(self):
                return open(self.filepath).read()
    '''
    propname = '__' + getter_function.__name__

    def fget(self):
        if hasattr(self, propname):
            return getattr(self, propname)
        value = getter_function(self)
        setattr(self, propname, value)
        return value

    return property(fget, doc=getter_function.__doc__)
