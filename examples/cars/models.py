import sys
import pathlib

src_module_dir = pathlib.Path(__file__).parent.parent.parent
sys.path.append(str(src_module_dir / 'src'))

from model import Model
from columns import Integer, Text, Real, Blob


class Car(Model):
    __table_name__ = 'cars'

    id = Integer(primary_key=True, autoincrement=True)
    brand = Text(default="chevrolet")
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
