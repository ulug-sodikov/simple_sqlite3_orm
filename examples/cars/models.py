from src.model import Model
from src.columns import Integer, Text, Real, Blob


class Car(Model):
    __table_name__ = 'cars'

    id = Integer(primary_key=True, autoincrement=True)
    brand = Text()
    model = Text()
    to_100 = Real()
    engine_id = Integer()
    horsepower = Integer()
    image = Blob()
    image_filename = Text()


class Engine(Model):
    __table_name__ = 'engines'

    id = Integer(primary_key=True, autoincrement=True)
    name = Text(unique=True)
