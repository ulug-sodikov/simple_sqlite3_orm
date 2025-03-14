import sqlite3
from functools import partial


def row_factory(model_cls, cursor, row):
    column_names = [i[0] for i in cursor.description]
    # Return model object if all columns (*) of table requested,
    # otherwise return dictionary.
    if (len(model_cls.column_names_) == len(column_names)
            and set(column_names) == set(model_cls.column_names_)):
        instance = model_cls()
        for col_name, col_value in zip(column_names, row):
            setattr(instance, col_name, col_value)

        return instance
    else:
        return dict(zip(column_names, row))


class Session:
    def __init__(self, path):
        self.path = path
        self.con = None

    def execute(self, query):
        if self.con is None:
            raise sqlite3.ProgrammingError("No connection!")

        sqlite3.row_factory = partial(row_factory, query.primary_model)
        return self.con.execute(*query).fetchall()

    def flush(self):
        if self.con is None:
            raise sqlite3.ProgrammingError("No connection!")

        self.con.commit()

    def rollback(self):
        if self.con is None:
            raise sqlite3.ProgrammingError("No connection!")

        self.con.rollback()

    def __enter__(self):
        self.con = sqlite3.connect(self.path)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.flush()
        else:
            self.rollback()

        self.con.close()
