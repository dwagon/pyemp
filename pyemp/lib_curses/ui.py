"""Curses UI"""

import curses
from typing import Optional
from .widget import Widget
from .keys import Keys


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
        if not self._focus:
            self._focus = self._widgets[0]  # TODO: Make selectable

    ###################################################################################
    def focus_widget(self, focus_on_widget: Widget) -> None:
        """Set focus on specific widget"""
        for widget in self._widgets:
            if widget._focus:
                widget.loseFocus()
            widget._focus = False
        focus_on_widget._focus = True
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
            self.hand_focus_change_input(ch)
            if self.has_finished():
                return

    ###################################################################################
    def hand_focus_change_input(self, ch: int):
        """Handle input that changes focus"""
        try:
            key_ch = Keys(ch)
        except ValueError:
            key_ch = Keys.KEY_NONE
        if key_ch == Keys.KEY_TAB:
            self.focus_next()
        elif key_ch == Keys.KEY_BTAB:
            self.focus_prev()

    ###################################################################################
    def handle_keyboard_event(self, key: int) -> bool:
        """Handle a keyboard event"""
        self.debug(f"handle_keyboard_event({key=})")
        if self._focus:
            return self._focus.handle_input(Keys(key))
        self.debug("unhandled input")
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
