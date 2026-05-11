"""List of entries"""

import curses
from collections import namedtuple
from typing import Optional

from .keys import Keys
from .widget import Widget

#######################################################################################
ENTRY = namedtuple("entry", ["value", "label"])


#######################################################################################
#######################################################################################
#######################################################################################
class Listbox(Widget):
    """A curses listbox"""

    ###################################################################################
    def __init__(self, parent: curses.window, begin_y: int, begin_x: int):
        super().__init__(parent=parent, begin_y=begin_y, begin_x=begin_x)
        self.entries: list[ENTRY] = []
        self.selected: Optional[int] = 0
        self.finished = False
        self.window = parent.derwin(0, 0, begin_y, begin_x)
        self.bindings = self.BINDINGS

    ###################################################################################
    def option_prev(self) -> None:
        """Previous option"""
        self.selected = max(0, self.selected - 1)

    ###################################################################################
    def option_next(self) -> None:
        """Next option"""
        self.selected = min(len(self.entries) - 1, self.selected + 1)

    ###################################################################################
    def option_select(self) -> None:
        """Select this option"""
        self.finished = True

    ###################################################################################
    def option_escape(self) -> None:
        """Quit without selecting anything"""
        self.selected = None
        self.finished = True

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
    def get(self) -> Optional[str]:
        """Return the value selected"""
        if self.selected:
            return self.entries[self.selected].value
        return None

    ###################################################################################
    def has_finished(self) -> bool:
        """Has the user selected the value"""
        return self.finished

    ###################################################################################
    BINDINGS = {
        Keys.KEY_W: option_prev,
        Keys.KEY_J: option_prev,
        Keys.KEY_UP: option_prev,
        Keys.KEY_S: option_next,
        Keys.KEY_K: option_next,
        Keys.KEY_DOWN: option_next,
        Keys.KEY_RETURN: option_select,
        Keys.KEY_ENTER: option_select,
        Keys.KEY_ESC: option_escape,
    }


# EOF
