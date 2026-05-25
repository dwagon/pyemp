"""Curses UI"""

import curses
from typing import Optional, Generator
from treelib import Tree

from .keys import Keys
from .widget import Widget
from .window import Window

ROOT_ID = "_root"


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
        self.widget_tree = Tree()
        self.widget_tree.create_node(identifier=ROOT_ID, data=self)
        self.root_window = None
        self._focus: Optional[Widget] = None
        lines = curses.LINES  # pylint: disable=no-member
        cols = curses.COLS  # pylint: disable=no-member
        self.root_window = self.stdscr.derwin(lines, cols, 0, 0)

    ###################################################################################
    def layout(self):
        """Layout the objects"""
        self.debug("layout()")
        for node in self.widget_tree.all_nodes():
            if node.identifier == ROOT_ID:
                continue
            node.data.layout()
        self._focus = list(self.children_widgets())[0]
        self.debug(f"{self._focus=}")

    ###################################################################################
    def focus_on(self, widget: Widget):
        """Set initial focus"""
        widget.focus = True

    ###################################################################################
    def focus_next(self) -> None:
        """Focus on the next child widget"""
        self.debug("focus_next()")

    ###################################################################################
    def focus_prev(self) -> None:
        """Focus on the previous child widget"""
        self.debug("focus_prev()")

    ###################################################################################
    def children_widgets(self) -> Generator[Widget, None, None]:
        """Return all children widgets"""
        for _ in self.widget_tree.children(ROOT_ID):
            yield _.data

    ###################################################################################
    def add(self, widget: Widget, name: str = "") -> Widget:
        """Add a widget to the screen"""
        if not isinstance(widget, Window):
            raise RuntimeError(f"Can only add Window() to UI, not {widget}")
        name = widget.name if widget.name else name
        if not name:
            name = widget.assign_name()
        widget.name = name
        widget.root_ui = self
        node = self.widget_tree.create_node(tag=name, data=widget, parent=ROOT_ID)
        widget.node_id = node.identifier
        widget.set_parent(self.root_window)
        self.debug(f"Adding {name=} {node=} {widget=}")

        return widget

    ###################################################################################
    def draw(self):
        """Nothing to draw"""
        pass

    ###################################################################################
    def mainloop(self):
        """Event loop for curses"""
        self.layout()
        while True:
            self.stdscr.clear()
            for node in self.widget_tree.all_nodes():
                node.data.draw()
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
