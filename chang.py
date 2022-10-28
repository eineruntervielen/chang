#!/usr/bin/env/ python
import argparse
import pathlib

from http.server import HTTPServer

from orm import SQLiteManager
from model import Task
from server import PORT_DEFAULT, HOSTNAME, ChangRequestHandler

DB_PATH = pathlib.Path.home() / ".chang/prod.sqlite"
SQLiteManager.set_connection(settings=DB_PATH)


def read_all():
    task_list = Task.objects.select()
    for t in task_list:
        print(t)


def insert():
    row = {}
    print("Label: ", end=None)
    row["label"] = input()
    print("Summary: ", end=None)
    row["summary"] = input()
    Task.objects.insert(row)


def serve():
    chang_server = HTTPServer((HOSTNAME, PORT_DEFAULT), ChangRequestHandler)
    print("Server started http://%s:%s" % (HOSTNAME, PORT_DEFAULT))
    try:
        chang_server.serve_forever()
    except KeyboardInterrupt:
        pass
    chang_server.server_close()
    print("Server stopped.")


def execute_mode(mode: str) -> None:
    match mode:
        case "read":
            read_all()
        case "insert":
            insert()
        case "serve":
            serve()
        case _:
            raise IOError("No mode presented")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["read", "insert", "serve"])
    args = parser.parse_args()
    execute_mode(args.mode)


if __name__ == "__main__":
    main()
