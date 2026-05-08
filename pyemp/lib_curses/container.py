"""Modal Curses Popup"""

import curses
from typing import Any

from .widget import Widget


#######################################################################################
#######################################################################################
#######################################################################################
class Container(Widget):
    """Container of Widgets"""

    def __init__(
        self,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.parent: curses.window = kwargs["parent"]
        self.nlines: int = kwargs.get("nlines")
        self.ncols: int = kwargs.get("ncols")
        self.begin_x: int = kwargs.get("begin_x", 0)
        self.begin_y: int = kwargs.get("begin_y", 0)
        self.parent: curses.window
        self.window = self.parent.derwin(
            self.nlines, self.ncols, self.begin_y, self.begin_x
        )
        self.border = kwargs.get("border", False)

        self._widgets = []

    ###################################################################################
    def derwin(self, *args, **kwargs):
        """Pass a derwin() call to the parent window"""
        return self.window.derwin(*args, **kwargs)

    ###################################################################################
    def getmaxyx(self) -> tuple[int, int]:
        """Return max y, max x of container"""
        return self.nlines, self.ncols

    ###################################################################################
    def add_widget(self, widget: Widget):
        """Add a widget"""
        self._widgets.append(widget)
        widget.parent = self.window

    ###################################################################################
    def draw(self):
        """Draw the window"""
        self.window.clear()
        if self.border:
            self.window.border()
        for widget in self._widgets:
            widget.draw()
        self.window.refresh()

    ###################################################################################
    def has_finished(self) -> bool:
        for widget in self._widgets:
            if widget.has_finished():
                return True
        return False

    ###################################################################################
    def mainloop(self):
        """Event loop for modal box"""
        while True:
            self.draw()
            # If you do window.getch() it can't handle escape sequences for unknown reasons
            ch = self.parent.getch()
            for widget in self._widgets:
                widget.handle_input(ch)
            if self.has_finished():
                return


# EOF
