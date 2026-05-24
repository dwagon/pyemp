"""Curses UI"""

import curses
import sys
from typing import Optional

from .keys import Keys
from .widget import Widget
from .window import Window


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
        self._widgets: list[Widget] = []
        self.root = None
        self._focus: Optional[Widget] = None

    ###################################################################################
    def layout(self):
        """Layout the objects"""
        lines = curses.LINES  # pylint: disable=no-member
        cols = curses.COLS  # pylint: disable=no-member
        self.root = self.stdscr.derwin(lines, cols, 0, 0)
        for widget in self._widgets:
            widget.layout()

    ###################################################################################
    def focus_on(self, widget: Widget):
        """Set initial focus"""
        self.debug(f"{self._widgets=} {widget=}")
        while widget not in self._widgets:
            widget = widget.parent_widget
        self._focus = self._widgets.index(widget)
        widget.focus = True

    ###################################################################################
    def focus_widget(self, focus_on_widget: Widget) -> None:
        """Set focus on specific widget"""
        for widget in self._widgets:
            if widget.focus:
                widget.loseFocus()
            widget.focus = False
        focus_on_widget.focus = True
        focus_on_widget.gainFocus()

    ###################################################################################
    def focus_next(self) -> None:
        """Move focus to next widget"""
        index = self._widgets.index(self._focus)
        looped = False
        while True:
            index += 1
            if index >= len(self._widgets):
                if looped:  # No suitable widgets
                    return
                looped = True
                index = 0
            if self._widgets[index].focusable:
                self.focus_widget(self._widgets[index])
                return

    ###################################################################################
    def focus_prev(self) -> None:
        """Move focus to prev widget"""
        index = self._widgets.index(self._focus)
        looped = False
        while True:
            index -= 1
            if index < 0:
                if looped:  # No suitable widgets
                    return
                looped = True
                index = len(self._widgets)
            if self._widgets[index].focusable:
                self.focus_widget(self._widgets[index])
                return

    ###################################################################################
    def add(self, widget: Widget, name: str = "") -> Widget:
        """Add a widget to the screen"""
        if not isinstance(widget, Window):
            print(
                f"Can only add Window() to UI, not {widget}", file=open("/tmp/err", "a")
            )
            sys.exit(2)
        if not name:
            name = widget.assign_name()
        widget.name = name
        self._widgets.append(widget)
        widget.set_parent(self.stdscr)
        return widget

    ###################################################################################
    def mainloop(self):
        """Event loop for curses"""
        self.layout()
        while True:
            self.stdscr.clear()
            for widget in self._widgets:
                widget.draw()
            curses.doupdate()

            # If you do window.getch() it can't handle escape sequences for unknown reasons
            ch = self.stdscr.getch()
            if ch == curses.KEY_MOUSE:
                self.handle_mouse_event()
            if self.handle_keyboard_event(ch):
                continue
            if self.handle_focus_change_input(ch):
                continue
            if self.has_finished():
                return

    ###################################################################################
    def handle_focus_change_input(self, ch: int) -> bool:
        """Handle input that changes focus"""
        try:
            key_ch = Keys(ch)
        except ValueError:
            self.debug(f"handle_focus_change_input({ch=})")
            key_ch = Keys.KEY_NONE
        if key_ch == Keys.KEY_TAB:
            self.focus_next()
            return True
        elif key_ch == Keys.KEY_BTAB:
            self.focus_prev()
            return True
        return False

    ###################################################################################
    def handle_keyboard_event(self, key: int) -> bool:
        """Handle a keyboard event"""
        if self._focus:
            try:
                keys_ch = Keys(key)
            except ValueError:
                self.debug(f"Non Key input {key}")
            else:
                return self._focus.handle_input(keys_ch)

        self.debug(f"unhandled input {key=}")
        return False

    ###################################################################################
    def handle_mouse_event(self):
        """Handle a mouse event"""
        for widget in self._widgets:
            widget.handle_mouse()

    ###################################################################################
    def has_finished(self) -> bool:
        """Has the widget finished doing its thing"""
        return False

    ###################################################################################
    def debug(self, msg: str):
        """Debug log"""
        with open("/tmp/widget_err", "a", encoding="utf-8") as outfh:
            outfh.write(f"UI: {msg}\n")


# EOF
