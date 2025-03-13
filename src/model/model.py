from .columns import Column
from ..utils import classproperty


class Model:
    query_ = "*"

    def __init__(self, *args, **kwargs):
        for col_name, value in zip(self.column_names_, args):
            setattr(self, col_name, value)

        for k, v in kwargs.items():
            if k in self.column_names_:
                setattr(self, k, v)
            else:
                raise TypeError(f"Unexpected keyword argument: {k}")

    def __getitem__(self, item):
        return self.column_names_[item]

    @classproperty
    def __table_name__(cls):
        """Override this property as an attribute in the subclass."""
        raise NotImplementedError

    @classproperty
    def column_names_(cls):
        return [k for k, v in cls.__dict__.items() if isinstance(v, Column)]

    @classproperty
    def model_(cls):
        return cls
