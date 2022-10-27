#!/usr/bin/env/ python
import argparse
import pathlib

from http.server import HTTPServer

from orm import BaseManager, Task
from server import PORT_DEFAULT, HOSTNAME, ChangRequestHandler

DB_PATH = pathlib.Path.home() / ".chang/prod.sqlite"
BaseManager.set_connection(settings=DB_PATH)


def read_all():
    task_list = Task.objects.read_all()
    for t in task_list:
        print(t)


def insert():
    print("Label: ", end=None)
    input()


def serve():
    webServer = HTTPServer((HOSTNAME, PORT_DEFAULT), ChangRequestHandler)
    print("Server started http://%s:%s" % (HOSTNAME, PORT_DEFAULT))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
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
