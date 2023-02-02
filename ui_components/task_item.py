def task_item(task):
    return f"<div " \
           f"class='task_item'" \
           f"draggable='true' ondragstart='dragStart(event)' ondrag='drag(event)' ondragend='dragEnd(event)'>{task.title}</div>"
