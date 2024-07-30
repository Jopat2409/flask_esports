"""Helper classes and functions for creating and executing database queries
"""
from typing import Generic, TypeVar

from .db import query_db, update_db

T = TypeVar("T")

class Query(Generic[T]):
    """Base SQL query class

    Args:
        Generic (_type_): _description_
    """

    def __init__(self, cast_function: callable, select: str, from_: str, where: str, args: tuple) -> None:
        self.cast = cast_function

        self.select_string = select
        self.from_string = from_
        self.where_string = where

        self.args = args

    def get_querystring(self) -> str:
        return f"SELECT {self.select_string} FROM {self.from_string}" + (f" WHERE {self.where_string};" if self.where_string else ";")

    def execute(self, one: bool = False) -> T | list[T] | None:
        """Execute this query against the working database

        Args:
            one (bool, optional): Whether to take one or a list of the records. Defaults to False.

        Returns:
            T | list[T] | None: _description_
        """
        db_records = query_db(self.get_querystring(), self.args, one)
        if db_records:
            return self.cast(db_records)
        return None

    def __repr__(self) -> str:
        return f"{self.get_querystring()}, args: {self.args}"

def _create_query_string(table: str, **kwargs) -> str:
    """Creates the query to get the correct coluns from the database

    Returns:
        str: _description_
    """
    return " and ".join(f"{table}.{i} = ?" for i in kwargs.keys())

def _create_column_select(tablename: str, c: str | tuple) -> str:
    if isinstance(c, str):
        return f"{tablename}.{c}"
    elif isinstance(c, tuple):
        return f"{tablename}.{c[0]} as {c[1]}"
    return ""

def _create_select_string(tablename: str, fields: list) -> str:
    return ', '.join(filter(lambda x: x != "", map(lambda x: _create_column_select(tablename, x), fields))) if fields else ''

def _join_selects(*queries) -> str:
    # combine selects
    return ", ".join(q.select_string for q in queries if q.select_string)

def _join_tables(*queries, on: str) -> str:
    querystrings = [queries[0].from_string, *[f"{q.from_string} ON ({' AND '.join(f'{queries[i].from_string}.{x} = {queries[i+1].from_string}.{x}' for x in on[i])})" for i, q in enumerate(queries[1:])]]
    return " INNER JOIN ".join(querystrings)


class BasicQuery(Query[T]):
    """A basic query is one that just filters database columns based on the keyword arguments passed, and returns all
    columns within the database that match the filters

    For example BasicQuery(Player, "valorant", player_id=10).execute() would get the first valorant player who's
    player_id is 10

    Args:
        Query: Parent `Query` class that implements the database execute method
    """

    def __init__(self, cls: T, game: str, **kwargs) -> None:
        """Creates a basic database search query based on the provided cls model

        Args:
            game (str): The game to query
        """
        super().__init__(
            cls.from_record,
            f"{cls.TABLENAME}.*",
            cls.TABLENAME,
            _create_query_string(cls.TABLENAME, source=game, **kwargs),
            tuple((game, *tuple(kwargs.values())))
        )


class LimitedQuery(Query[T]):
    """A limited query has all the features of a basic query, but allows for selecting specific columns from the database
    A limited query with no `cols` argument supplied is no different to a `BasicQuery`

    If you want the columns to be renamed when the SQL query is executed (IE SELECT id AS player_id), then supply the
    column as a tuple containing (col_name, rename_to). `cols=["player_id", ("forename", "name")]` would corresponds to
    `SELECT player_id, forename AS name...`

    Args:
        Query: Parent `Query` class that implements the database execute method
    """

    def __init__(self, cls, game: int, cols: list = ["*"], **kwargs):
        super().__init__(
            cls.from_record,
            _create_select_string(cls.TABLENAME, cols),
            cls.TABLENAME,
            _create_query_string(cls.TABLENAME, source=game, **kwargs),
            tuple((game, *tuple(kwargs.values())))
        )


class JoinQuery(Query[T]):
    """A query that mimics the behaviour of an inner join
    Use this query to join other `Query` subtypes such as `BasicQuery` and `LimitedQuery`

    Args:
        Query (_type_): _description_
    """

    def __init__(self,*queries: list[Query], on=[], cast_function: callable = lambda x: x) -> None:

        if (len(queries) - 1) != len(on):
            print(queries, on)
            raise ValueError("The length of the on argument must be the same as the number of queries to be joined - 1")

        super().__init__(
            cast_function,
            _join_selects(*queries),
            _join_tables(*queries, on=on),
            queries[0].where_string,
            tuple(arg for q in queries for arg in q.args)
        )
        print(self)

def insert_one(obj) -> bool:
    args = obj.to_record()
    update_db(f"INSERT INTO {obj.TABLENAME} VALUES ({', '.join('?' for _ in args)});", args=args)

def insert_many(objs: list) -> bool:
    args = [obj.to_record() for obj in objs]
    update_db(f"INSERT INTO {objs[0].TABLENAME} VALUES " + ", ".join(f"({', '.join('?' for _ in args[0])})" for _ in objs) + ";", args=tuple(e for obj_data in args for e in obj_data))
