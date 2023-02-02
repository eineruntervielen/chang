#!/usr/bin/env/ python
import re
import argparse
import pathlib
import sqlite3

from difflib import get_close_matches
from functools import partial
from typing import NewType, NamedTuple
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler

from ui_components import *

DB_PATH = pathlib.Path.home() / ".chang/prod.db"
HOSTNAME = "localhost"
MODES = ("select", "insert", "delete", "serve")
PORT_DEFAULT = 3131
QUERY_NEW_TABLE = (
    "CREATE TABLE IF NOT EXISTS task(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, summary TEXT, label TEXT, state TEXT);")
Query = NewType('Query', str)
STATES = ("open", "started", "closed")
INDEX_STRING = """<!DOCTYPE html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="main.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            font-family: monospace;
            color: rgb(50, 50, 50)
        }

        main {
            min-height: 100vh;
            background: cadetblue;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .task_list {
            padding: 0.25rem;
            display: flex;
            flex-direction: column;
            border: 2px solid black;
        }

        .task_item {
            margin: 0.25rem;
            padding: 0.25rem;
            background: gainsboro;
        }

        .task_item:hover {
            background: cyan;
            cursor: pointer;

        }
    </style>
</head>
<body>
{{%app_entry%}}
</body>
<script>
    drag = () => {
        console.log("dragging")
    }
    dragStart = () => {
        console.log("Started dragging")
    }
    dragEnd = () => {
        console.log("End dragging")
    }
</script>
</html>"""


class UserInput(NamedTuple):
    title: str
    summary: str
    label: str
    state: str


class Task(NamedTuple):
    id: int
    title: str
    summary: str
    label: str
    state: str


def render_layout(replacement: str):
    return re.sub(pattern="{{%app_entry%}}", repl=replacement, string=INDEX_STRING)


class ChangRequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        all_tasks = query_select_all()
        print(all_tasks)
        self.wfile.write(bytes(render_layout(replacement=app(all_tasks)), "utf-8"))


def build_query_select(table: str, columns: str | list[str]) -> Query:
    """Merges chosen columns and the table name to create sql query for
    select statement.

    >>> build_query_select(table="task", columns="*")
    'SELECT * FROM task;'
    >>> build_query_select(table="task", columns=["id", "name"])
    'SELECT id,name FROM task;'
    >>> build_query_select(table="task", columns="")
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


def build_query_delete(table: str, attribute: str, value: str) -> Query:
    """Merges chosen columns and the table name to create sql query for
    delete statement.

    >>> build_query_delete(table="task", attribute="id", value="1")
    'DELETE FROM task WHERE id = 1;'

    :param table: Name of the table to delete from
    :param attribute:
    :param value:
    :return: SQL string DELETE query
    """
    return Query(f"DELETE FROM {table} WHERE {attribute} = {value};")


def build_query_insert(table: str, row: dict) -> Query:
    """Merges user input data to create input statement.

    >>> row_test = {'Id': 1, 'Name': 'Hello'}
    >>> build_query_insert(table="task", row=row_test)
    "INSERT INTO task(Id, Name) VALUES ('1', 'Hello');"

    :param table: Name of the table to delete from
    :param row:
    :return: SQL string INSERT query
    """
    fields = ", ".join(row.keys())
    values = ", ".join([f'\'{v}\'' for v in row.values()])
    return Query(f"INSERT INTO {table}({fields}) VALUES ({values});")


query_select_all = partial(build_query_select, table="task", columns="*")
query_delete_by_id = partial(build_query_delete, table="task", attribute="id")
query_delete_by_state = partial(build_query_delete, table="task", attribute="state")


def get_user_input() -> UserInput:
    fields = UserInput._fields
    d = dict(zip(fields, list(map(lambda x: input(), map(lambda c: print(str(c).capitalize()), fields)))))
    return UserInput(**d)


def get_user_input_delete() -> str:
    print("Which Id?")
    user_input = input()
    return user_input


def execute_query(query):
    with sqlite3.connect(DB_PATH) as con:
        return con.execute(query).fetchall()


def mode_select() -> list[Task]:
    query = query_select_all()
    result = execute_query(query)
    return list(map(lambda r: Task(*r), result))


def mode_delete(user_input) -> None:
    query = query_delete_by_id(value=user_input)
    execute_query(query)


def mode_insert(user_input: UserInput) -> None:
    query = build_query_insert(table="task", row=user_input._asdict())
    execute_query(query)


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
                execute_query(QUERY_NEW_TABLE)
                print("DB and table created")
            except:
                SystemError("Table could not be created")
    else:
        print(f"The database already exists here: {DB_PATH}")


def execute_mode(chosen_mode: str) -> None:
    match chosen_mode:
        case "select":
            tasks = mode_select()
            list(map(lambda x: print(x), tasks))
        case "insert":
            user_input = get_user_input()
            mode_insert(user_input)
        case "delete":
            user_input = get_user_input_delete()
            mode_delete(user_input)
        case "serve":
            mode_serve()
        case "setup":
            mode_setup()


def correct_mode(mode_chosen: str) -> str:
    """Checks if the selected mode from the user is valid. Raises ValueError
    otherwise.

    :param mode_chosen: Selected mode
    """
    if not mode_chosen:
        raise IOError("No mode presented")
    if not isinstance(mode_chosen, str):
        raise ValueError("Mode must be string")
    possible_matches = get_close_matches(word=mode_chosen, possibilities=MODES, n=1)
    if possible_matches:
        interpreted_mode = str(possible_matches[0])
        return interpreted_mode
    else:
        raise ValueError("No mode present because you wrote crap")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    # parser = argparse.ArgumentParser()
    # parser.add_argument("mode", choices=MODES)
    # args = parser.parse_args()
    # execute_mode(args.mode)
    execute_mode("select")
