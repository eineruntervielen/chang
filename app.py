import argparse
from orm import BaseManager, Task

DB_PATH = "dev.sqlite"


def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(name_or_flags="mode", choices=["read", "update"])
    parser.parse_args()


if __name__ == "__main__":
    BaseManager.set_connection(settings=DB_PATH)
    task_list = Task.objects.read()
    t1 = Task(task_id=3, label="irgendwas")
    Task.objects.create(t1)
    print(task_list)
