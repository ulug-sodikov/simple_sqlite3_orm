import sqlite3
from functools import partial
from contextlib import contextmanager

from simple_sqlite3_orm.statements import InsertStatement


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

    def insert(self, model):
        """Insert a row into the table."""
        if self.con is None:
            raise sqlite3.ProgrammingError("No connection!")

        with start_transaction(self):
            stmt = InsertStatement(model)
            cur = self.con.execute(*stmt)

        # Assign id of newly created row to model.
        for column in model.column_names_:
            # get column descriptor, not column value.
            col = getattr(model.__class__, column)
            if col.primary_key:
                setattr(model, column, cur.lastrowid)
                break

        return model

    def commit(self):
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
            self.commit()
        else:
            self.rollback()

        self.con.close()


@contextmanager
def start_transaction(session):
    try:
        yield session
    except Exception:
        session.rollback()
    else:
        session.commit()
