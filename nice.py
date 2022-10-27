from enum import Enum
from tkinter import HORIZONTAL


class BoxDrawingsLight(Enum):
    down_and_right = "┌"
    horizontal = "─"
    down_and_left = "┐"
    up_and_right = "└"
    up_and_left = "┘"


box = BoxDrawingsLight
print(box.down_and_right.value + box.horizontal.value * 5)