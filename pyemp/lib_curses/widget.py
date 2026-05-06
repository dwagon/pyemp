"""Parent class for widgets"""

import curses
from typing import Callable, Any, Self


#######################################################################################
#######################################################################################
#######################################################################################
class Widget:
    """Generic Widget Class"""

    def __init__(self, parent: curses.window, begin_y: int, begin_x: int):
        self.parent = parent
        self.begin_y = begin_y
        self.begin_x = begin_x
        self.bindings: dict[Any, Callable[[Self], None]] = {}

    def draw(self) -> None:
        """Draw the Widget"""
        raise NotImplementedError

    def handle_input(self, key: int) -> None:
        """Handle character input"""
        if key in self.bindings:
            return self.bindings[key](self)
        return None

    def has_finished(self) -> bool:
        """Has the widget finished doing its thing"""
        raise NotImplementedError


# EOF
