# Columns should have "model_" attribute (reference to model).
# Columns should have "query_" attribute (column name).
# Models should have "__table_name__" class attribute.
# Aggregate functions like SUM should act like column objects.


class SelectStatement:
    """
    Class for creating SQL select queries.

    Typical usage:
        SelectStatement().select(Model.column)
    """
    _query_parts = ("SELECT", "FROM", "JOIN", "ON", "WHERE")

    def __init__(self):
        self._query = {}
        self._parameters = {}
        self.primary_model = None

    def select(self, *columns, distinct=False):
        """
        Implements SQL "SELECT column(s)" query part.
        Also implements "FROM table" part of query if columns are from
        the same table.
        """
        if not columns:
            raise TypeError("columns are not provided.")

        select_query_parts = ["SELECT"]
        if distinct:
            select_query_parts.append("DISTINCT")

        models = set()
        columns_query_parts = []
        for column in columns:
            models.add(column.model_)
            columns_query_parts.append(column.query_)

        select_query_parts.append(', '.join(columns_query_parts))
        self._query["SELECT"] = " ".join(select_query_parts)

        if len(models) == 1:
            model = models.pop()
            self.primary_model = model
            self._query["FROM"] = f"FROM {model.__table_name__}"

        return self

    def from_(self, model):
        """
        Implements SQL "FROM table" query part.

        select() method identifies querying table automatically by
        looking into columns, thus this method is only useful if
        there are columns of multiple tables and join statement.
        """
        self.primary_model = model
        self._query['FROM'] = f"FROM {model.__table_name__}"

        return self

    def join(self, model, left=False):
        """Implements SQL "JOIN table" query part."""
        if model is self.primary_model:
            raise ValueError('Attempted to join the same tabel.')

        query_parts = []
        if left:
            query_parts.append("LEFT")


        query_parts.append(f"JOIN {model.__table_name__}")
        self._query['JOIN'] = ' '.join(query_parts)

        return self

    def on(self, column, matching_column):
        """
        Implements SQL "ON table.column = another_table.column" query part.
        """
        self._query['ON'] = f'ON {column.query_} = {matching_column.query_}'

        return self

    def where(self, condition):
        """
        Implements SQL "WHERE condition AND/OR another_condition AND/OR ...;"
        query part.
        """
        self._query['WHERE'] = f'WHERE {condition.query_}'
        self._parameters.update(condition.parameters_)

        return self

    @property
    def query(self):
        """Get raw SQL query."""
        query_parts = []
        for part in self._query_parts:
            if part in self._query:
                query_parts.append(self._query[part])

        return " ".join(query_parts)

    @property
    def parameters(self):
        return self._parameters

    def __iter__(self):
        yield self.query
        yield self.parameters


class InsertStatement:
    """
    Class for creating SQL insert statement.

    Typical usage:
        InsertStatement(model).statement
    """
    def __init__(self, model):
        self.model = model

    @property
    def inserting_columns(self):
        return [col for col in self.model.column_names_
                             if getattr(self.model, col, None) is not None]

    @property
    def parameters(self):
        return {f'param_{col}': getattr(self.model, col)
                for col in self.inserting_columns}

    @property
    def statement(self):
        """Get raw SQL query."""
        named_placeholders = [f':{p}' for p in self.parameters]

        return f"""
            INSERT INTO {self.model.__table_name__}
            ({', '.join(self.inserting_columns)})
            VALUES ({', '.join(named_placeholders)})
        """

    def __iter__(self):
        yield self.statement
        yield self.parameters


class UpdateStatement:
    """
    Class for creating SQL update statement.

    Typical usage:
        UpdateStatement(model).statement
    """
    def __init__(self, model):
        self.model = model

    @property
    def pk_column_name(self):
        pk_col_name = None
        for col_name in self.model.column_names_:
            col_obj = getattr(self.model.__class__, col_name)
            if col_obj.primary_key:
                pk_col_name = col_name
                break

        return pk_col_name

    @property
    def parameters(self):
        return {f'param_{col_name}': getattr(self.model, col_name)
                for col_name in self.model.column_names_}

    @property
    def statement(self):
        updating_cols = self.model.column_names_
        updating_cols.remove(self.pk_column_name)
        stmt_parts = [f'{col} = :param_{col}' for col in updating_cols]

        return f"""
            UPDATE {self.model.__table_name__}
            SET {', '.join(stmt_parts)}
            WHERE {self.pk_column_name} = :param_{self.pk_column_name}
        """

    def __iter__(self):
        yield self.statement
        yield self.parameters


def select(*args, **kwargs):
    """Shortcut for creating select query."""
    return SelectStatement().select(*args, **kwargs)
