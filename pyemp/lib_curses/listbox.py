"""List of entries"""

import curses
from collections import namedtuple
from typing import Optional, Any

from .keys import Keys
from .widget import Widget, FitType

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
        self._selected: Optional[int] = 0
        self.bindings = self.BINDINGS
        self.fit = FitType.MIN_FIT

    ###################################################################################
    def option_prev(self) -> None:
        """Previous option"""
        self._selected = max(0, self._selected - 1)

    ###################################################################################
    def option_next(self) -> None:
        """Next option"""
        self._selected = min(len(self.entries) - 1, self._selected + 1)

    ###################################################################################
    def option_select(self) -> None:
        """Select this option"""
        # TODO

    ###################################################################################
    def option_escape(self) -> None:
        """Quit without selecting anything"""
        self._selected = None

    ###################################################################################
    def add_entry(self, val: str, entry: str):
        """Add an entry to the listbox"""
        self.entries.append(ENTRY(val, entry))

    ###################################################################################
    @property
    def required_height(self) -> int:
        """Height of widget"""
        return len(self.entries)

    ###################################################################################
    @property
    def required_width(self) -> int:
        """Width of widget"""
        # +1 for curses being weird
        return self._max_width() + 1

    ###################################################################################
    def _max_width(self) -> int:
        """Return the widest entry"""
        return max(len(_.label) for _ in self.entries)

    ###################################################################################
    def draw(self):
        """Draw the widget"""
        for y, line in enumerate(self.entries):
            if y == self._selected:
                attr = curses.A_REVERSE
            else:
                attr = curses.A_NORMAL
            self._window.addstr(y, 0, line.label, attr)

    ###################################################################################
    def get(self) -> Optional[str]:
        """Return the value selected"""
        if self._selected:
            return self.entries[self._selected].value
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
