from .task_list import task_list


def app(all_tasks):
    states = ['Open', 'Started', 'Closed']
    return f"<main>{''.join(task_list(list(filter(lambda x: x.state == s, all_tasks))) for s in states)}</main>"
