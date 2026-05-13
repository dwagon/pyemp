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
        self.nlines: int = kwargs.get(
            "nlines", curses.LINES  # pylint: disable=no-member
        )
        self.ncols: int = kwargs.get("ncols", curses.COLS)  # pylint: disable=no-member
        self.begin_x: int = kwargs.get("begin_x", 0)
        self.begin_y: int = kwargs.get("begin_y", 0)
        self.window = None
        self.border_window = None
        self.border = kwargs.get("border", False)

        self._widgets: dict[str, Widget] = {}

    ###################################################################################
    def layout(self):
        """Setup - outer canvas for borders,etc, inner canvas for widgets"""
        self.border_window = self.parent.derwin(
            self.nlines, self.ncols, self.begin_y, self.begin_x
        )
        nlines, ncols, begin_y, begin_x = self.padded_size()
        self.window = self.border_window.derwin(nlines, ncols, begin_y, begin_x)
        for widget in self._widgets.values():
            widget.parent = self.window
            widget.parent.move(begin_y, begin_x)
            widget.layout()

    ###################################################################################
    def padded_size(self) -> tuple[int, int, int, int]:
        """How big the inner canvas should be based on the borders"""
        nlines = self.nlines
        ncols = self.ncols
        begin_y = self.begin_y
        begin_x = self.begin_x
        if self.border:
            nlines -= 2
            ncols -= 2
            begin_y += 1
            begin_x += 1

        return nlines, ncols, begin_y, begin_x

    ###################################################################################
    def add(self, name: str, widget: Widget) -> Widget:
        """Add a widget to the container"""
        self._widgets[name] = widget
        self._widgets[name].name = name
        return widget

    ###################################################################################
    def delete(self, name: str):
        """Remove a widget from the container"""
        del self._widgets[name]

    ###################################################################################
    def derwin(self, *args, **kwargs):
        """Pass a derwin() call to the parent window"""
        return self.window.derwin(*args, **kwargs)

    ###################################################################################
    def getmaxyx(self) -> tuple[int, int]:
        """Return max y, max x of container"""
        return self.nlines, self.ncols

    ###################################################################################
    def draw(self):
        """Draw the window"""
        self.window.clear()
        if self.border:
            self.border_window.border()
        for widget in self._widgets.values():
            widget.draw()
        self.window.refresh()


# EOF
