"""Simple String Label Widget"""

import curses
from .widget import Widget


#######################################################################################
#######################################################################################
#######################################################################################
class Label(Widget):
    """Label Widget"""

    def __init__(self, parent: curses.window, begin_y: int, begin_x: int, label: str):
        super().__init__(parent, begin_y, begin_x)
        self.label = label

    def draw(self):
        """Draw the label"""
        self.parent.addstr(self.begin_y, self.begin_x, self.label)

    def handle_input(self, ch: int) -> bool:
        """Labels don't listen to inputs"""
        return False

    def has_finished(self) -> bool:
        """Labels don't finish"""
        return False


# EOF
