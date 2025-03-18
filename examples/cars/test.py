from simple_sqlite3_orm.statements import select
from simple_sqlite3_orm.session import Session

from models import Car, Engine


def main():
    q = (
        select(Engine.name, Car.to_100)
        .from_(Car)
        .join(Engine)
        .on(Car.engine_id, Engine.id)
        .where(
            Car.brand.in_('toyota', 'nissan', 'audi') | Car.engine_id.in_(1, 4, 7)
        )
    )
    print(*q)
    print(Engine.column_names_)
    print(Car.column_names_)

    with Session('database.db') as session:
        mclaren = Car()
        mclaren.brand = 'McLaren'
        mclaren.model = 'GT'
        mclaren.to_100 = 3.2
        mclaren.engine_id = 45
        mclaren.horsepower = 612

        engine = Engine()
        engine.id = 45
        engine.name = '4.0-liter twin-turbocharged V8 engine'

        print(mclaren.id)
        session.insert(mclaren)
        print(mclaren.id)


if __name__ == '__main__':
    main()
