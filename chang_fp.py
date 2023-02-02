#!/usr/bin/env/ python
import argparse
import collections
import pathlib
import sqlite3

from contextlib import closing

from typing import NewType, NamedTuple
from http.server import HTTPServer
from chang_handler import PORT_DEFAULT, HOSTNAME, ChangRequestHandler

DB_PATH = pathlib.Path.home() / ".chang/prod.db"
Query = NewType('Query', str)

FIELDS = ("title", "summary", "label", "state")
MODES = ("select", "insert", "delete", "serve")
STATES = ("open", "started", "closed")
QUERY_NEW_TABLE: Query = Query(
    "CREATE TABLE IF NOT EXISTS task(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, summary TEXT, label TEXT, state TEXT);")


class Task(NamedTuple):
    id: int
    title: str
    summary: str
    label: str
    state: str


def _get_user_input() -> dict[str, str]:
    return dict(zip(
        FIELDS,
        list(map(lambda x: input(), map(lambda c: print(str(c).capitalize()), FIELDS))))
    )


def _build_query_select(table: str, columns: str | list[str]):
    """Merges chosen columns and the table name to create sql query for
    select statement.

    >>> _build_query_select(table="task", columns="*")
    'SELECT * FROM task;'
    >>> _build_query_select(table="task", columns=["id", "name"])
    'SELECT id,name FROM task;'
    >>> _build_query_select(table="task", columns="")
    Traceback (most recent call last):
    ...
    ValueError: Columns can not be empty

    :param table: Name of the table to select from
    :param columns: Names of the columns to select from
    :return: SQL string SELECT query
    """
    if not columns:
        raise ValueError(f"Columns can not be empty")
    return Query(f"SELECT {','.join(columns)} FROM {table};")


def _build_query_delete(table: str, attribute: str, value: str) -> str:
    """Merges chosen columns and the table name to create sql query for
    delete statement.

    >>> _build_query_delete(table="task", attribute="task_id", value="1")
    'DELETE FROM task WHERE task_id = 1;'

    :param table: Name of the table to delete from
    :param attribute:
    :param value:
    :return: SQL string DELETE query
    """
    return Query(f"DELETE FROM {table} WHERE {attribute} = {value};")


def _build_query_insert(table: str, row: NamedTuple) -> str:
    fields = ", ".join(row.keys())
    values = ", ".join([f'\'{v}\'' for v in row.values()])
    return f"INSERT INTO {table}({fields}) VALUES ({values})"


def _execute_query(query):
    with closing(sqlite3.connect(DB_PATH)) as con:
        con.cursor().execute(query)
        con.commit()


def mode_select(table: str, columns: str):
    query = _build_query_select(table=table, columns=columns)
    with closing(sqlite3.connect(DB_PATH)) as con:
        tasks = list(map(lambda t: Task(*t), con.cursor().execute(query).fetchall()))
        print(tasks)


def mode_delete():
    query = _build_query_delete(table="task", attribute="task_id", value="13")
    _execute_query(query)


def mode_insert():
    row = _get_user_input()
    query = _build_query_insert(row)
    _execute_query(query)


def mode_serve():
    chang_server = HTTPServer((HOSTNAME, PORT_DEFAULT), ChangRequestHandler)
    print(f"Server started http://{HOSTNAME}:{PORT_DEFAULT}")
    try:
        chang_server.serve_forever()
    except KeyboardInterrupt:
        pass
    chang_server.server_close()
    print("Server stopped.")


def mode_setup():
    if not pathlib.Path(DB_PATH).exists():
        print("Would you like to setup a database? [Y/n]")
        answer = input()
        if answer == 'Y':
            try:
                _execute_query(QUERY_NEW_TABLE)
                print("DB and table created")
            except:
                SystemError("Table could not be created")
    else:
        print(f"The database already exists here: {DB_PATH}")


def execute_mode(chosen_mode: str) -> None:
    match chosen_mode:
        case "select":
            mode_select(table="task", columns="*", )
        case "insert":
            mode_insert()
        case "delete":
            mode_delete()
        case "serve":
            mode_serve()
        case "setup":
            mode_setup()


def correct_mode(mode_chosen: str) -> None:
    """Checks if the selected mode from the user is valid. Raises ValueError
    otherwise.

    :param mode_chosen: Selected mode
    """
    if not mode_chosen:
        raise IOError("No mode presented")
    if not isinstance(mode_chosen, str):
        raise ValueError("Mode must be string")
    if not isinstance(mode_chosen, str):
        raise ValueError("Mode must be string")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=MODES)
    args = parser.parse_args()
    execute_mode(args.mode)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    mode = "select"
    execute_mode(mode)
