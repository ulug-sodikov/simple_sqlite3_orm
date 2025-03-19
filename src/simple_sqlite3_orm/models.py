from simple_sqlite3_orm.columns import Column
from simple_sqlite3_orm.utils import classproperty


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
        column_name = self.column_names_[item]
        return getattr(self, column_name)

    @classproperty
    def __table_name__(cls):
        """Override this property as an attribute in the subclass."""
        raise NotImplementedError

    @classproperty
    def column_names_(cls):
        return [k for k, v in cls.__dict__.items() if isinstance(v, Column)]

    @classproperty
    def pk_column_name_(cls):
        pk_col_name = None
        for col_name in cls.column_names_:
            col = getattr(cls, col_name)
            if col.primary_key:
                pk_col_name = col_name
                break

        return pk_col_name

    @classproperty
    def model_(cls):
        return cls
