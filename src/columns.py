from utils import classproperty


class Column:
    def __init__(
        self,
        default=None,
        primary_key=False,
        unique=False,
        autoincrement=False,
        not_null=True,
    ):
        self.default = default
        self.primary_key = primary_key
        self.unique = unique
        self.autoincrement = autoincrement
        self.not_null = not_null
        self.attrname = None
        self.model_ = None
        self.query_ = None

    def __set_name__(self, owner, name):
        self.model_ = owner
        self.query_ = f'{owner.__table_name__}.{name}'
        self.attrname = name

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self.attrname] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance.__dict__.get(self.attrname)

    @classproperty
    def datatype(self):
        """Override this property as an attribute in the subclass."""
        raise NotImplementedError

    @classproperty
    def sql_datatype(self):
        """Override this property as an attribute in the subclass."""
        raise NotImplementedError

    @property
    def sql_constrains(self):
        query_parts = []
        if self.primary_key:
            query_parts.append("PRIMARY KEY")

        if self.autoincrement:
            query_parts.append("AUTOINCREMENT")

        if self.unique:
            query_parts.append("UNIQUE")

        if self.not_null:
            query_parts.append("NOT NULL")

        return ' '.join(query_parts)

    @property
    def sql_default(self):
        if self.default is None:
            return None

        if self.datatype is str:
            return f'DEFAULT "{self.default}"'

        if self.datatype is int or self.datatype is float:
            return f'DEFAULT {self.default}'

    def validate(self, value):
        if not isinstance(self.datatype, value):
            raise TypeError(f'Invalid type for {self.attrname}.')


class Integer(Column):
    datatype = int
    sql_datatype = 'INTEGER'


class Real(Column):
    datatype = float
    sql_datatype = 'REAL'


class Text(Column):
    datatype = str
    sql_datatype = 'TEXT'


class Blob(Column):
    datatype = bytes
    sql_datatype = 'BLOB'
