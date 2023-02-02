"""
Reference: https://unicode-table.com/en/blocks/box-drawing/
https://www.geeksforgeeks.org/print-colors-python-terminal/

Wrapping lines and shortening if table to small  https://docs.python.org/3/library/textwrap.html
"""
import textwrap
import logging
from os import get_terminal_size
from enum import Enum
from typing import Any

logging.basicConfig(level=logging.DEBUG)


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


class ColorForeground(Enum):
    yellow = "\033[93m"
    end = "\033[00m"


def printc(text: str, fg: str, bg: str):
    print(paint(text, fg, bg))


def paint(text: str, fg: str, bg: str):
    return f"{fg.value}{text}{Color.end.value}"


def table(rows: list[dict[str, Any]], column_headers: list[str] = None) -> None:
    # max_width = get_terminal_size().columns
    cols_to_row_entries = {col: []
                           for col in rows[0].keys()}
    for row in rows:
        for col, entry in row.items():
            cols_to_row_entries.get(col).append(entry)
    print(cols_to_row_entries)
    cols_to_max_width = {
        col: max([len(entry) for entry in cols_to_row_entries.get(col)]) for col in cols_to_row_entries
    }
    print(cols_to_max_width)


def print_table(column_headers: list[str], rows: list):
    """Prints a formatted table to stdout using unicode characters from the range...
    """
    max_window_width = get_terminal_size().columns
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


if __name__ == '__main__':
    table(rows=[
        {'Id': 'fklajsdf slkaj sdöfjasd', 'Title': "askdlfjaslkdfjsda"},
        {'Id': 'slkaj sdöfjasd', 'Title': "askdlfjaslkdfjsda"},
        {'Id': 'fklajsdf sdöfjasd', 'Title': "askdlslkdfjsda sdk j"},
        {'Id': 'slkaj ', 'Title': "askdlfjaslsda k jdskjsdfa "},
    ])
