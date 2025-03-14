import sys
import os
import importlib
import inspect
import sqlite3
from pathlib import Path

from model import Model


## Fix imports, otherwise this can happen
## <class 'src.model.Model'> <class 'model.Model'>


def import_from_path(models_path):
    models_path = Path(os.getcwd()).joinpath(models_path)
    sys.path.append(str(models_path.parent))

    return importlib.import_module(models_path.name.removesuffix('.py'))


def create_table_stmt(model):
    col_stmts = []

    for col_name in model.column_names_:
        col = getattr(model, col_name)
        stmt = f'{col.attrname} {col.sql_datatype} {col.sql_constrains}'

        if col.sql_default is not None:
            stmt += f" {col.sql_default}"

        col_stmts.append(stmt)

    return f"CREATE TABLE {model.__table_name__} ({', '.join(col_stmts)})"


def create_tables(models_file_path):
    module = import_from_path(models_file_path)

    models = inspect.getmembers(
        module,
        lambda m: inspect.isclass(m) and issubclass(m, Model) and m is not Model
    )
    models = (model[1] for model in models)
    con = sqlite3.connect('database.db')

    for model in models:
        con.execute(create_table_stmt(model))

    con.close()


if __name__ == '__main__':
    try:
        models_file_path = sys.argv[1]
    except IndexError:
        print('Provide models file path.')
        exit()
    else:
        create_tables(models_file_path)
