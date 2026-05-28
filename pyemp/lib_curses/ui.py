"""Curses UI"""

import curses
from typing import Optional, cast

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
        self.node_id = ROOT_ID
        self.widget_tree.create_node(identifier=self.node_id, data=self)
        self.root_window = None
        lines = curses.LINES  # pylint: disable=no-member
        cols = curses.COLS  # pylint: disable=no-member
        self.root_window = self.stdscr.derwin(lines, cols, 0, 0)
        self.bindings = {
            Keys.KEY_RIGHT: self.focus_next,
            Keys.KEY_TAB: self.focus_next,
            Keys.KEY_LEFT: self.focus_prev,
            Keys.KEY_BTAB: self.focus_prev,
        }

    ###################################################################################
    def all_widgets(self) -> list[Widget]:
        """Return all widgets"""
        widgets = [
            _.data for _ in self.widget_tree.all_nodes() if _.identifier != ROOT_ID
        ]
        return widgets

    ###################################################################################
    def layout(self):
        """Layout the objects"""
        self.child_window().layout()
        self.debug(self.widget_tree.show(stdout=False))

    ###################################################################################
    def focus_on_widget(self, focus_on_widget: Widget) -> None:
        """Set focus on specific widget"""
        for widget in self.all_widgets():
            if widget.focus:
                widget.loseFocus()
            widget.focus = False
        focus_on_widget.focus = True
        focus_on_widget.gainFocus()

    ###################################################################################
    def which_widget_has_focus(self) -> Optional[Widget]:
        """Which widget has focus"""
        for widget in self.all_widgets():
            if widget.focus:
                return widget
        return None

    ###################################################################################
    def focus_next(self) -> None:
        """Move focus to next widget"""
        focussed_widget = self.which_widget_has_focus()
        all_widgets = self.all_widgets()
        if not focussed_widget:
            focussed_widget = all_widgets[0]

        # Which child has focus
        next_widget_index = -1
        for num, widget in enumerate(all_widgets):
            if widget == focussed_widget:
                next_widget_index = num

        count = len(all_widgets)
        while count:
            next_widget_index = (next_widget_index + 1) % len(all_widgets)
            if all_widgets[next_widget_index].focusable:
                self.focus_on_widget(all_widgets[next_widget_index])
                return
            count -= 1

    ###################################################################################
    def focus_prev(self) -> None:
        """Move focus to prev widget"""
        focussed_widget = self.which_widget_has_focus()
        all_widgets = self.all_widgets()
        if not focussed_widget:
            focussed_widget = all_widgets[0]

        # Which child has focus
        next_widget_index = -1
        for num, widget in enumerate(all_widgets):
            if widget == focussed_widget:
                next_widget_index = num

        count = len(all_widgets)
        while count:
            next_widget_index = (next_widget_index + (len(all_widgets) - 1)) % len(
                all_widgets
            )
            if all_widgets[next_widget_index].focusable:
                self.focus_on_widget(all_widgets[next_widget_index])
                return
            count += 1

    ###################################################################################
    def child_window(self) -> Widget:
        """Return the child window of UI"""
        return list(self.widget_tree.children(ROOT_ID))[0].data

    ###################################################################################
    def add(self, widget: Widget, name: str = "") -> Widget:
        """Add a widget to the screen"""
        if not isinstance(widget, Window):
            raise RuntimeError(f"Can only add Window() to UI, not {widget}")
        if self.widget_tree.size() > 1:
            raise RuntimeError(
                f"Can only have one child of root UI, not {self.widget_tree.size()}"
            )
        name = widget.name if widget.name else name
        if not name:
            name = widget.assign_name()
        widget.name = name
        widget.root_ui = self
        node = self.widget_tree.create_node(tag=name, data=widget, parent=ROOT_ID)
        widget.node_id = node.identifier
        widget.set_parent(self.root_window)

        return widget

    ###################################################################################
    def draw(self):
        """Draw all the things"""
        self.stdscr.clear()
        self.child_window().draw()
        curses.doupdate()

    ###################################################################################
    def mainloop(self):
        """Event loop for curses"""
        self.layout()
        while True:
            self.draw()
            # If you do window.getch() it can't handle escape sequences for unknown reasons
            ch = self.stdscr.getch()
            if ch == curses.KEY_MOUSE:
                self.handle_mouse_input()
                continue
            try:
                key_ch = Keys(ch)
            except ValueError:
                self.debug(f"Non Key input {ch}")
                continue
            self.handle_key_input(key_ch)

    ###################################################################################
    def handle_mouse_input(self):
        """Handle mouse input"""
        mouse = curses.getmouse()
        _, x, y, _, bstate = mouse
        self.debug(f"handle_mouse_input() {x}, {y}, {bstate}")
        for node in self.widget_tree.leaves():
            widget = cast(Widget, node.data)
            if widget.enclose(y, x):
                if widget.mouse_bindings:
                    widget.handle_mouse_event(x, y, bstate)

    ###################################################################################
    def handle_key_input(self, key: Keys):
        """Handle keyboard input"""
        if widget := self.which_widget_has_focus():
            if widget.handle_keyboard_input(key):
                return
            while self.widget_tree.parent(widget.node_id):
                widget = self.widget_tree.parent(widget.node_id).data
                if widget.handle_keyboard_input(key):
                    return
        self.handle_keyboard_input(key)

    ###################################################################################
    def handle_keyboard_input(self, key: Keys) -> bool:
        """Handle character input - return if event handled"""
        if key in self.bindings:
            self.bindings[key]()
            return True
        return False

    ###################################################################################
    def debug(self, msg: str):
        """Debug log"""
        with open("/tmp/widget_err", "a", encoding="utf-8") as outfh:
            outfh.write(f"UI: {msg}\n")


# EOF
