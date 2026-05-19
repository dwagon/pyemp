"""List of entries"""

import curses
from collections import namedtuple
from typing import Optional, Any

from .keys import Keys
from .widget import Widget, Dimension

#######################################################################################
ENTRY = namedtuple("entry", ["value", "label"])


#######################################################################################
#######################################################################################
#######################################################################################
class Listbox(Widget):
    """A curses listbox"""

    ###################################################################################
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.entries: list[ENTRY] = []
        self.selected: Optional[int] = 0
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
        # TODO

    ###################################################################################
    def option_escape(self) -> None:
        """Quit without selecting anything"""
        self.selected = None

    ###################################################################################
    def add_entry(self, val: str, entry: str):
        """Add an entry to the listbox"""
        self.entries.append(ENTRY(val, entry))

    ###################################################################################
    def calculate_height(self, requested: Dimension, border_win: bool = False) -> int:
        """Height of listbox"""
        return len(self.entries) + (2 if self.border else 0)

    ###################################################################################
    def calculate_width(self, requested: Dimension, border_win: bool = False) -> int:
        """Width of listbox"""
        return (
            self.max_width() + 1 + (2 if self.border else 0)
        )  # +1 for curses weirdness

    ###################################################################################
    def max_width(self) -> int:
        """Return the widest entry"""
        return max(len(_.label) for _ in self.entries)

    ###################################################################################
    def draw(self):
        """Draw the widget"""
        for y, line in enumerate(self.entries):
            if y == self.selected:
                attr = curses.A_REVERSE
            else:
                attr = curses.A_NORMAL
            self._window.addstr(y, 0, line.label, attr)

    ###################################################################################
    def get(self) -> Optional[str]:
        """Return the value selected"""
        if self.selected:
            return self.entries[self.selected].value
        return None

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
