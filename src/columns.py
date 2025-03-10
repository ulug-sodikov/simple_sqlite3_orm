from .utils import classproperty


_NO_VALUE = object()


class Column:
    def __init__(
        self,
        default=_NO_VALUE,
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
        self._attrname = None
        self.model_ = None
        self.query_ = None

    def __set_name__(self, owner, name):
        self.model_ = owner
        self.query_ = name
        self._attrname = name

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self._attrname] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance.__dict__.get(self._attrname)

    @classproperty
    def datatype(self):
        """Override this property as an attribute in the subclass."""
        raise NotImplementedError

    def validate(self, value):
        if not isinstance(self.datatype, value):
            raise TypeError(f'Invalid type for {self._attrname}.')


class Integer(Column):
    datatype = int


class Real(Column):
    datatype = float


class Text(Column):
    datatype = str


class Blob(Column):
    datatype = bytes
