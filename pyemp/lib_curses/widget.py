"""Parent class for widgets"""

import curses


#######################################################################################
#######################################################################################
#######################################################################################
class Widget:
    """Generic Widget Class"""

    def __init__(self, parent: curses.window, begin_y: int, begin_x: int):
        self.parent = parent
        self.begin_y = begin_y
        self.begin_x = begin_x
        self.finished = False

    def draw(self) -> None:
        """Draw the Widget"""
        raise NotImplementedError

    def handle_input(self, ch: int) -> bool:
        """Handle character input - return True if handled"""
        raise NotImplementedError

    def has_finished(self) -> bool:
        """Has the widget finished doing its thing"""
        raise NotImplementedError


# EOF
