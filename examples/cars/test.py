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

    engine = Engine(name="3.0-liter twin-turbocharged straight-six")
    supra = Car(brand='Toyota', model='Supra MK4', to_100=5.3, horsepower=321)

    with Session('database.db') as session:
        session.insert(engine)
        supra.engine_id = engine.id

        print(f'mclaren.id: {supra.id}')    # No id yet.
        session.insert(supra)
        print(f'mclaren.id: {supra.id}')    # Got id after insertion.


if __name__ == '__main__':
    main()
