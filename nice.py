"""
Reference: https://unicode-table.com/en/blocks/box-drawing/
https://www.geeksforgeeks.org/print-colors-python-terminal/

Wrapping lines and shortening if table to small  https://docs.python.org/3/library/textwrap.html
"""
import textwrap
from os import get_terminal_size
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


class Color(Enum):
    yellow = "\033[93m"
    end = "\033[00m"


def printc(text: str, fg_color: str):
    if not isinstance(fg_color, Color):
        raise ValueError(f"Expected {fg_color} to be one of {Color.__members__}")
    print(f"{fg_color.value}{text}{Color.end.value}")


def printcr(text: str, fg_color: str):
    if not isinstance(fg_color, Color):
        raise ValueError(f"Expected {fg_color} to be one of {Color.__members__}")
    return f"{fg_color.value}{text}{Color.end.value}"


def out_nice_table(column_headers: list[str], rows: list):
    min_col_width = {
        col: len(col) for col in column_headers
    }
    # print(min_col_width)
    terminal_size = get_terminal_size()
    # print(terminal_size.columns)
    box = BoxDrawingsLight
    # First row with upper border
    print(
        box.down_and_right.value
        + box.horizontal.value * 6
        + box.down_and_horizontal.value
        + box.horizontal.value * 20
        + box.down_and_horizontal.value
        + box.horizontal.value * 60
        + box.down_and_horizontal.value
        + box.horizontal.value * 20
        + box.down_and_horizontal.value
        + box.horizontal.value * 20
        + box.down_and_left.value
    )
    print(
        box.vertical.value
        + f"{'Id': ^6}"
        + box.vertical.value
        + f"{'Title': ^20}"
        + box.vertical.value
        + f"{'Summary': ^60}"
        + box.vertical.value
        + f"{'Label': ^20}"
        + box.vertical.value
        + f"{'State': ^20}"
        + box.vertical.value
    )
    print(
        box.vertical_and_right.value
        + box.horizontal.value * 6
        + box.vertical_and_horizontal.value
        + box.horizontal.value * 20
        + box.vertical_and_horizontal.value
        + box.horizontal.value * 60
        + box.vertical_and_horizontal.value
        + box.horizontal.value * 20
        + box.vertical_and_horizontal.value
        + box.horizontal.value * 20
        + box.vertical_and_left.value
    )
    for row in rows:
        summary = row.summary
        if len(summary) > 60:
            summary = textwrap.shorten(row.summary, width=60, placeholder="...")
        print(
            box.vertical.value
            + f"{row.task_id: ^6}"
            + box.vertical.value
            + f"{row.title: ^20}"
            + box.vertical.value
            + f"{summary: <60}"
            + box.vertical.value
            + f"{row.label: ^20}"
            + box.vertical.value
            + f"{row.state: ^20}"
            + box.vertical.value
        )  # smelly fuck
    print(
        box.up_and_right.value
        + box.horizontal.value * 6
        + box.up_and_horizontal.value
        + box.horizontal.value * 20
        + box.up_and_horizontal.value
        + box.horizontal.value * 60
        + box.up_and_horizontal.value
        + box.horizontal.value * 20
        + box.up_and_horizontal.value
        + box.horizontal.value * 20
        + box.up_and_left.value
    )
