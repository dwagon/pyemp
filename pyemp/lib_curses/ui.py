"""Curses UI"""

import curses
from typing import Any, Optional
from .widget import Widget


#######################################################################################
#######################################################################################
#######################################################################################
class UI:
    """Parent Curses interface"""

    def __init__(self, stdscr: Optional[curses.window] = None):
        if stdscr:
            self.stdscr = stdscr
        else:
            self.stdscr = curses.initscr()
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        curses.curs_set(0)  # Invisible cursor
        self.stdscr.keypad(True)
        self._widgets: dict[str, Widget] = {}
        self.root = None

    ###################################################################################
    def layout(self):
        """Layout the objects"""
        lines = curses.LINES  # pylint: disable=no-member
        cols = curses.COLS  # pylint: disable=no-member
        self.root = self.stdscr.derwin(lines, cols, 0, 0)
        for widget in self._widgets.values():
            widget.layout()

    ###################################################################################
    def add(self, name: str, widget: Widget) -> Widget:
        """Add a widget to the screen"""
        self._widgets[name] = widget
        widget.name = name
        widget.parent = self.stdscr
        return widget

    ###################################################################################
    def mainloop(self):
        """Event loop for curses"""
        self.layout()
        while True:
            for widget in self._widgets.values():
                widget.draw()
            curses.doupdate()

            # If you do window.getch() it can't handle escape sequences for unknown reasons
            ch = self.stdscr.getch()
            if ch == curses.KEY_MOUSE:
                self.handle_mouse_event()
            self.handle_keyboard_event(ch)
            if self.has_finished():
                return

    ###################################################################################
    def handle_keyboard_event(self, key: int):
        """Handle a keyboard event"""
        for widget in self._widgets.values():
            widget.handle_input(key)

    ###################################################################################
    def handle_mouse_event(self):
        """Handle a mouse event"""
        for widget in self._widgets.values():
            widget.handle_mouse()

    ###################################################################################
    def has_finished(self) -> bool:
        """Has the widget finished doing its thing"""
        return False


# EOF
