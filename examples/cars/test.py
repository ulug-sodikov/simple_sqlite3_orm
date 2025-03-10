import pathlib
import sys

module_path = pathlib.Path(__file__).parent.parent.parent
sys.path.append(str(module_path))

from src.queries import select
from examples.cars.models import Car, Engine


def main():
    q = select(Engine.name, Car.to_100).from_(Car).join(Engine).on(Car.engine_id, Engine.id)
    print(*q)
    print(Engine.column_names_)
    print(Car.column_names_)


if __name__ == '__main__':
    main()
