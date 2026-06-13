"""Curses UI"""

import curses
from typing import Optional, cast

from treelib import Tree

from .keys import Keys
from .widget import Widget
from .dialog import Dialog, ErrorDialog

ROOT_ID = "_root"


#######################################################################################
#######################################################################################
#######################################################################################
class UI(Widget):
    """Parent Curses interface
    Handles focus
    """

    def __init__(self, stdscr: Optional[curses.window] = None, **kwargs):
        if stdscr:
            self.stdscr = stdscr
        else:
            self.stdscr = curses.initscr()
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        curses.curs_set(0)  # Invisible cursor
        self.stdscr.keypad(True)
        self._widget_tree = Tree()
        self.name = "_UI"
        self.modal_focus_widget: Optional[Widget] = None
        self.node_id = ROOT_ID
        self.widget_tree.create_node(identifier=self.node_id, data=self)
        self.root_window = None
        lines = curses.LINES  # pylint: disable=no-member
        cols = curses.COLS  # pylint: disable=no-member
        self.root_window = self.stdscr.derwin(lines, cols, 0, 0)
        super().__init__(**kwargs)
        self.node_id = ROOT_ID
        self.bindings.update(
            {
                Keys.KEY_RIGHT: self.focus_next,
                Keys.KEY_TAB: self.focus_next,
                Keys.KEY_LEFT: self.focus_prev,
                Keys.KEY_BTAB: self.focus_prev,
            }
        )

    ###################################################################################
    @property
    def widget_tree(self) -> Tree:
        """Shortcut to the widget tree"""
        return self._widget_tree

    ###################################################################################
    def all_widgets(self, root: Tree = None) -> list[Widget]:
        """Return all widgets"""
        if not root:
            root = self.widget_tree
        widgets = [_.data for _ in root.all_nodes() if _.identifier != ROOT_ID]
        return widgets

    ###################################################################################
    def all_focusable_widgets(self) -> list[Widget]:
        """Return all widgets that are focusable"""

        if self.modal_focus_widget:
            tree = self.widget_tree.subtree(nid=self.modal_focus_widget.node_id)
        else:
            tree = None
        widgets = [_ for _ in self.all_widgets(tree) if _.focusable]
        return widgets

    ###################################################################################
    def layout(self):
        """Layout the objects"""
        self.which_widget_has_focus()  # Assign focus if none
        for widget in self.child_windows():
            self.debug(f"Layout for {widget=}")
            widget.layout()

    ###################################################################################
    def focus_on_widget(self, focus_widget: Widget) -> None:
        """Set focus on specific widget"""
        for widget in self.all_focusable_widgets():
            if focus_widget != widget and widget.focus:
                widget.loseFocus()
            widget.focus = False
        focus_widget.focus = True
        focus_widget.gainFocus()
        self.debug(f"focus_on_widget({focus_widget=})")

    ###################################################################################
    def which_widget_has_focus(self) -> Optional[Widget]:
        """Which widget has focus - if none then set if possible"""
        for widget in self.all_focusable_widgets():
            if widget.focus:
                return widget
        # No focussed widget found
        for widget in self.all_focusable_widgets():
            return widget
        # No focusable widgets found
        return None

    ###################################################################################
    def focus_next(self) -> None:
        """Move focus to next widget"""
        focussed_widget = self.which_widget_has_focus()
        all_widgets = self.all_focusable_widgets()

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
        all_widgets = self.all_focusable_widgets()

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
    def child_windows(self) -> list[Widget]:
        """Return the child window of UI"""
        return list(_.data for _ in self.widget_tree.children(ROOT_ID))

    ###################################################################################
    def add(self, widget: Widget, name: str = "") -> Widget:
        """Add a widget to the screen"""
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
    def delete(self, widget: Widget) -> None:
        """Delete a widget and all its children"""
        subtree = self.widget_tree.remove_subtree(nid=widget.node_id)
        for node in subtree.all_nodes():
            widg = cast(Widget, node.data)
            if widg.focus:
                if widg.modal_focus:
                    self.modal_focus_widget = None
                self.focus_on_widget(self.all_focusable_widgets()[0])  # Make cleverer

    ###################################################################################
    def draw(self):
        """Draw all the things"""
        self.stdscr.clear()
        for widget in self.child_windows():
            widget.draw()
        curses.doupdate()
        self.stdscr.refresh()

    ###################################################################################
    def update_callbacks(self):
        """Process all widgets update callbacks"""
        all_widgets = self.all_widgets()
        for widget in all_widgets:
            if widget.update_callback:
                widget.update_callback()

    ###################################################################################
    def mainloop(self):
        """Event loop for curses"""
        while True:
            self.draw()
            self.update_callbacks()
            self.handle_input()
            self.debug(f"{self=}\n{self._widget_tree.show(stdout=False)}")

    ###################################################################################
    def handle_input(self):
        """Handle mouse and keyboard input"""
        # If you do window.getch() it can't handle escape sequences for unknown reasons
        ch = self.stdscr.getch()
        if ch == curses.KEY_MOUSE:
            self.handle_mouse_input()
            return
        try:
            key_ch = Keys(ch)
        except ValueError:
            self.debug(f"Non Key input {ch}")
            return
        self.handle_key_input(key_ch)

    ###################################################################################
    def handle_mouse_input(self):
        """Handle mouse input"""
        mouse = curses.getmouse()
        _, x, y, _, bstate = mouse
        for node in self.widget_tree.leaves():
            widget = cast(Widget, node.data)
            if widget.enclose(y, x):
                if widget.mouse_bindings:
                    widget.handle_mouse_event(x, y, bstate)

    ###################################################################################
    def handle_key_input(self, key: Keys):
        """Handle keyboard input for all widgets"""
        self.debug(f"handle_key_input({key=})")
        if widget := self.which_widget_has_focus():
            self.debug(f"Focussed on {widget}")
            if widget.handle_keyboard_input(key):
                return
            while self.widget_tree.parent(widget.node_id):
                widget = self.widget_tree.parent(widget.node_id).data
                if widget.handle_keyboard_input(key):
                    return
        self.handle_keyboard_input(key)

    ###################################################################################
    @property
    def required_height(self) -> int:
        """Whole screen"""
        return curses.LINES  # pylint: disable=no-member

    ###################################################################################
    @property
    def required_width(self) -> int:
        """Whole screen"""
        return curses.COLS  # pylint: disable=no-member

    ###################################################################################
    def add_dialog(self, **kwargs) -> Widget:
        """Add a Dialog"""
        d = Dialog(**kwargs)
        self.add(d)
        return d

    ###################################################################################
    def add_error_dialog(self, **kwargs) -> Widget:
        """Add an error dialog"""
        d = ErrorDialog(**kwargs)
        self.add(d)
        return d


# EOF
