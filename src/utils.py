class classproperty:
    """
    Class that behaves like @property and @classmethod decorators
    combined.
    """
    def __init__(self, func):
        self._func = func

    def __get__(self, instance, owner):
        return self._func(owner)
