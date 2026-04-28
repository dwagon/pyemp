"""Curses based button"""

import curses


#######################################################################################
class Button:
    """Button"""

    def __init__(self, label: str, y: int, x: int, window: curses.window):
        self.label = label
        self.y = y
        self.x = x
        self.window = window.derwin(3, len(label) + 2, self.y, self.x)

    def draw(self):
        """Draw the button"""
        self.window.clear()
        self.window.border()
        self.window.addstr(1, 1, self.label)

    def is_clicked(self, mouse_y: int, mouse_x: int) -> bool:
        """Did the user click on the button"""
        min_y, min_x = self.window.getbegyx()
        max_y, max_x = self.window.getmaxyx()
        print(
            f"DBG {min_x=} {min_y=} {max_x+min_x=} {max_y+min_y=} {mouse_x=} {mouse_y=}",
            file=open("/tmp/err", "a"),
        )
        if min_y < mouse_y < max_y + min_y and min_x < mouse_x < max_x + min_x:
            return True
        return False

    @property
    def width(self) -> int:
        """Width of the button"""
        return len(self.label) + 2


# EOF
