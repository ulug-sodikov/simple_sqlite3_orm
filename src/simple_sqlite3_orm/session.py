import sqlite3
from functools import partial
from contextlib import contextmanager

from simple_sqlite3_orm.statements import InsertStatement, UpdateStatement


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
        self.con = sqlite3.connect(path)

    def execute(self, query):
        if self.con is None:
            raise sqlite3.ProgrammingError("No connection!")

        self.con.row_factory = partial(row_factory, query.primary_model)
        return self.con.execute(*query).fetchall()

    def insert(self, model):
        """Insert a row into the table."""
        if self.con is None:
            raise sqlite3.ProgrammingError("No connection!")

        with start_transaction(self):
            stmt = InsertStatement(model)
            cur = self.con.execute(*stmt)

        # Assign id of newly created row to model.
        pk_col_name = stmt.pk_column_name_
        if pk_col_name is not None:
            setattr(model, pk_col_name, cur.lastrowid)

        return model

    def update(self, model):
        """Update a row in table."""
        pk_col_name = model.pk_column_name_

        if pk_col_name is None:
            raise Exception("Can't update row that doesn't have pk column!")

        pk_col_value = getattr(model, pk_col_name)
        if pk_col_value is None:
            raise Exception(
                "Trying to update a row that doesn't exist in the table!"
            )

        with start_transaction(self):
            stmt = UpdateStatement(model)
            self.con.execute(*stmt)

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
        raise
    else:
        session.commit()
