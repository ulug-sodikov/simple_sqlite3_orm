from simple_sqlite3_orm.models import Model
from simple_sqlite3_orm.columns import Integer, Text, Real, Blob


class Car(Model):
    __table_name__ = 'cars'

    id = Integer(primary_key=True, autoincrement=True)
    brand = Text(default="chevrolet")
    model = Text()
    to_100 = Real()
    engine_id = Integer()
    horsepower = Integer()


class Engine(Model):
    __table_name__ = 'engines'

    id = Integer(primary_key=True, autoincrement=True)
    name = Text(unique=True)
