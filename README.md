# Simple ORM
Simple Python ORM for sqlite3.
## Prerequisite
- To use this library you need to create file `simple_sqlite3_orm.pth`
  in your `python3.X/site-pachages/` directory. This file should 
  contain path to `simple_sqlite3_orm/src/`.
  `simple_sqlite3_orm.pth` file content example:
```
/home/username/PycharmProjects/simple_sqlite3_orm/src/
```
## Usage
```
from orm.model import (
    Model, Integer, Blob, 
    Text
)    


class Car(Model):
    __table_name__ = 'cars'

    id = Integer(primary_key=True, autoincrement=True)
    brand = Text(default="Tesla")
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

- To create tables use the following command:
```
python3 -m simple_sqlite3_orm.create_tables my_models.py
```
here `my_models.py` is a file which contains your models.
