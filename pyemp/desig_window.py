"""Designate Sector code"""

import curses
from .lib_curses.modal import Modal
from .lib_curses.listbox import Listbox
from .lib_curses.label import Label
from .lib_curses.widget import Widget
from .sector import DESIG_KEY_MAP
from .misc import debug


#######################################################################################
#######################################################################################
#######################################################################################
class Desig_Window:
    """Designate Sector Window"""

    def __init__(
        self,
        x: int,
        y: int,
        window: curses.window,
        nlines: int,
        ncols: int,
        begin_y: int = 0,
        begin_x: int = 0,
    ):
        self.x = x
        self.y = y
        self.parent_window = window
        self.begin_y = begin_y
        self.begin_x = begin_x
        self.nlines = nlines
        self.ncols = ncols
        self.widgets: list[Widget] = []
        self.new_desig: str = ""
        self.modal = Modal(
            self.parent_window, self.nlines, self.ncols, self.begin_y, self.begin_x
        )
        self.listbox = None
        self.init_widgets()

    ###################################################################################
    def init_widgets(self):
        """Add widgets"""
        self.listbox = Listbox(self.modal.window, 3, 1)
        for desig, descr in DESIG_KEY_MAP.items():
            if desig in ("?", ".", "^", "s", "-", "~", "\\"):  # Can't be designated as
                continue
            self.listbox.add_entry(desig, f"{desig} {descr}")
        self.modal.add_widget(
            Label(
                self.modal.window,
                1,
                1,
                f"Designate Sector ({self.x}, {self.y})",
            ),
        )
        self.modal.add_widget(self.listbox)

    ###################################################################################
    def mainloop(self):
        """Event loop"""

        self.modal.mainloop()
        ans = self.listbox.get()
        self.new_desig = ans

    ###################################################################################
    def get(self) -> str:
        """Return result"""
        return self.new_desig


# EOF
