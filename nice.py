"""
Reference: https://unicode-table.com/en/blocks/box-drawing/
"""
from enum import Enum


class BoxDrawingsLight(Enum):
    down_and_right = "┌"
    horizontal = "─"
    vertical_and_horizontal = "┼"
    vertical = "│"
    vertical_and_right = "├"
    vertical_and_left = "┤"
    down_and_horizontal = "┬"
    down_and_left = "┐"
    up_and_right = "└"
    up_and_left = "┘"
    up_and_horizontal = "┴"


def out_nice_table(column_headers: list[str], rows: list):
    box = BoxDrawingsLight
    print(
        box.down_and_right.value
        + box.horizontal.value * 5
        + box.down_and_horizontal.value
        + box.horizontal.value * 20
        + box.down_and_horizontal.value
        + box.horizontal.value * 80
        + box.down_and_left.value
    )
    print(
        box.vertical.value
        + f"{'Id': ^5}"
        + box.vertical.value
        + f"{'Label': ^20}"
        + box.vertical.value
        + f"{'Summary': ^80}"
        + box.vertical.value
    )
    print(
        box.vertical_and_right.value
        + box.horizontal.value *5 
        + box.vertical_and_horizontal.value
        + box.horizontal.value * 20
        + box.vertical_and_horizontal.value
        + box.horizontal.value * 80
        + box.vertical_and_left.value
    )
    for row in rows:
        print(
            box.vertical.value
            + f"{row.task_id: ^5}"
            + box.vertical.value
            + f"{row.label: ^20}"
            + box.vertical.value
            + f"{row.summary: ^80}"
            + box.vertical.value
        )  # smelly fuck
    print(
        box.up_and_right.value
        + box.horizontal.value * 5
        + box.up_and_horizontal.value
        + box.horizontal.value * 20
        + box.up_and_horizontal.value
        + box.horizontal.value * 80
        + box.up_and_left.value
    )
