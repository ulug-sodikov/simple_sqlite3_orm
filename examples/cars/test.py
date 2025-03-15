from simple_sqlite3_orm.statements import select

from models import Car, Engine


def main():
    q = select(Engine.name, Car.to_100).from_(Car).join(Engine).on(Car.engine_id, Engine.id)
    print(*q)
    print(Engine.column_names_)
    print(Car.column_names_)


if __name__ == '__main__':
    main()
