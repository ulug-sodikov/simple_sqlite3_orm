# Simple ORM
Simple Python ORM for sqlite3.
## Usage
```
from orm.model import (
    Model, Integer, Blob, 
    Text
)    


class Car(Model):
    __table_name__ = 'cars'

    id = Integer(primary_key=True, autoincrement=True)
    brand = Text()
    model = Text()
    engine_id = Integer()
    horsepower = Integer()
    price = Integer()
    image = Blob()
    image_filename = Text()


class Engine(Model):
    __table_name__ = 'engines'

    id = Integer(primary_key=True, autoincrement=True)
    name = Text(unique=True)


with Session('database.db') as session:
    # Select all BMW cars that cost less than 200k $ and output them.
    res = select(Car.brand, Car.model).where(
        Car.price <= 200000, Car.brand == "BMW"
    )
    for row in res:
        print(*row)
        
```