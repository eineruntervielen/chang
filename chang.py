#!/usr/bin/env/ python
import argparse
import pathlib

from orm import BaseManager, Task

DB_PATH = pathlib.Path.home() / ".chang/prod.sqlite"
BaseManager.set_connection(settings=DB_PATH)

def execute_mode(mode: str) -> None:
    match mode:
        case "read":
            task_list = Task.objects.read()
            for t in task_list:
                print(t)
        case _:
            raise IOError("No mode presented")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["read"])
    args = parser.parse_args()
    execute_mode(args.mode)


if __name__ == "__main__":
    main()
