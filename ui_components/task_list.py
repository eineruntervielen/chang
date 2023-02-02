from .task_item import task_item


def task_list(tasks: list):
    return f"<div class='task_list'>{''.join(task_item(t) for t in tasks)}</div>"
