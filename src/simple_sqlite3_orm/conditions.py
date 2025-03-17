import itertools


# For generating unique nums for named placeholders.
num_generator = itertools.count()


class ConditionOperationsMixin:
    """Implements SQL condition operations."""
    def __eq__(self, queryable):
        return Condition('=', self, queryable)

    def __ne__(self, queryable):
        return Condition('!=', self, queryable)

    def __gt__(self, queryable):
        return Condition('>', self, queryable)

    def __ge__(self, queryable):
        return Condition('>=', self, queryable)

    def __lt__(self, queryable):
        return Condition('<', self, queryable)

    def __le__(self, queryable):
        return Condition('<=', self, queryable)

    def __and__(self, queryable):
        return Condition('AND', self, queryable)

    def in_(self, *values):
        return Condition('IN', self, values)

    def not_in(self, *values):
        return Condition('NOT IN', self, values)

    def like(self, value):
        return Condition('LIKE', self, value)

    def not_like(self, value):
        return Condition('NOT LIKE', self, value)


class Condition(ConditionOperationsMixin):
    """
    An object representing an SQL condition statement part in SQL query.
    """
    def __init__(self, operator, queryable, other_queryable):
        self.query_, self.parameters_ = self.create_condition_query(
            operator, queryable, other_queryable
        )

    def create_condition_query(
        self, operator, queryable, other_queryable
    ):
        """
        Returns a tuple of SQL condition query part and placeholder parameters.
        """
        query_first_part, first_param = self.to_query(queryable)
        query_second_part, second_param = self.to_query(other_queryable)

        return (
            f'{query_first_part} {operator} {query_second_part}',
            {**first_param, **second_param}
        )

    def to_query(self, queryable):
        """
        Returns a tuple of SQL condition query part and placeholder parameters
        for a single unit (Condition, Column or other values).
        """
        query = getattr(queryable, 'query_', None)
        if query is not None:
            return query, getattr(queryable, 'parameters_', {})

        key = f'param{next(num_generator)}'
        return f':{key}', {key: queryable}
