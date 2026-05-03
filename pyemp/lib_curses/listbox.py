"""List of entries"""

import curses
from collections import namedtuple
from .widget import Widget
from .keys import Keys
from ..misc import debug

#######################################################################################
ENTRY = namedtuple("entry", ["value", "label"])


#######################################################################################
#######################################################################################
#######################################################################################
class Listbox(Widget):
    """A curses listbox"""

    ###################################################################################
    def __init__(self, parent: curses.window, begin_y: int, begin_x: int):
        super().__init__(parent, begin_y, begin_x)
        self.entries: list[ENTRY] = []
        self.selected = 0
        self.window = parent.derwin(0, 0, begin_y, begin_x)

    ###################################################################################
    def add_entry(self, val: str, entry: str):
        """Add an entry to the listbox"""
        self.entries.append(ENTRY(val, entry))
        self.window.resize(len(self.entries), self.max_width())

    ###################################################################################
    def max_width(self) -> int:
        """Return the widest entry"""
        return max(len(_.label) for _ in self.entries)

    ###################################################################################
    def draw(self):
        """Draw the widget"""
        self.window.clear()
        for y, line in enumerate(self.entries):
            if y == self.selected:
                attr = curses.A_REVERSE
            else:
                attr = curses.A_NORMAL
            self.window.addstr(y, 0, line.label, attr)

    ###################################################################################
    def get(self) -> str:
        """Return the value selected"""
        return self.entries[self.selected].value

    ###################################################################################
    def has_finished(self) -> bool:
        """Has the user selected the value"""
        debug(f"{self.finished=}")
        return self.finished

    ###################################################################################
    def handle_input(self, ch: int) -> bool:
        """Handle keys"""
        debug(f"Input {ch=} {chr(ch)}")
        match ch:
            case Keys.KEY_W:
                self.selected = max(0, self.selected - 1)
            case Keys.KEY_S:
                self.selected = min(len(self.entries) - 1, self.selected + 1)
            case Keys.KEY_ENTER:
                self.finished = True
            case _:
                return False
        return True


# EOF
