"""Container of other widgets"""

import curses
from typing import Any, Optional, Generator
from .keys import Keys
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
        self.bindings = {
            Keys.KEY_TAB: self.focus_next,
            Keys.KEY_BTAB: self.focus_prev,
        }
        self.bindings.update(kwargs.get("bindings", {}))

    ###################################################################################
    def children_widgets(self) -> Generator[Widget, None, None]:
        """Return all children widgets"""
        for _ in self.widget_tree.children(self.node_id):
            yield _.data

    ###################################################################################
    def layout(self):
        """Setup - outer canvas for borders,etc, inner canvas for widgets"""
        super().layout()
        for widget in self.children_widgets():
            widget.set_parent(self._window)
            widget.layout()

    ###################################################################################
    def add(self, widget: Widget, name: str = "") -> Widget:
        """Add a widget to the container"""
        name = widget.name if widget.name else name
        if not name:
            name = widget.assign_name()
        widget.name = name

        widget.root_ui = self.root_ui
        node = self.widget_tree.create_node(tag=name, data=widget, parent=self.node_id)
        widget.node_id = node.identifier
        return widget

    ###################################################################################
    def delete(self, name: str):
        """Remove a widget from the container"""
        for node in self.root_ui.children(self.node_id):
            if node.name == name:
                self.root_ui.widget_tree.remove_node(node.identifier)

    ###################################################################################
    @property
    def required_height(self) -> int:
        """required_height of container"""
        if children := list(self.children_widgets()):
            h = max(_.required_height for _ in children)
        else:
            h = 1  # Min size
        return h

    ###################################################################################
    @property
    def required_width(self) -> int:
        """required_width of container"""
        if children := list(self.children_widgets()):
            w = max(_.required_width for _ in children)
        else:
            w = 1  # Min size
        return w

    ###################################################################################
    def draw(self):
        """Draw the window"""
        super().draw()
        for widget in self.children_widgets():
            if self.focus:
                self._window.attron(curses.A_BOLD)
            else:
                self._window.attroff(curses.A_BOLD)
            widget.draw()

    ###################################################################################
    def handle_input(self, key: Keys) -> bool:
        """Handle character input"""

        if key in self.bindings:
            self.debug(f"{self.name} handle_input({key=})")
            self.bindings[key]()
            return True
        if widget := self.which_widget_has_focus():
            self.debug(f"Giving input to {widget=}")
            return widget.handle_input(key)
        return False

    ###################################################################################
    def focus_on_widget(self, focus_on_widget: Widget) -> None:
        """Set focus on specific widget"""
        for widget in self.children_widgets():
            if widget.focus:
                widget.loseFocus()
            widget.focus = False
        focus_on_widget.focus = True
        focus_on_widget.gainFocus()

    ###################################################################################
    def which_widget_has_focus(self) -> Optional[Widget]:
        """Which widget has focus"""
        for widget in self.children_widgets():
            if widget.focus:
                return widget
        return None

    ###################################################################################
    def focus_next(self) -> None:
        """Move focus to next widget"""
        focussed_widget = self.which_widget_has_focus()
        children = list(self.children_widgets())
        if not focussed_widget:
            focussed_widget = children[0]

        # Which child has focus
        next_widget_index = -1
        for num, widget in enumerate(children):
            if widget == focussed_widget:
                next_widget_index = num

        while True:
            next_widget_index = (next_widget_index + 1) % len(children)
            if children[next_widget_index].focusable:
                self.focus_on_widget(children[next_widget_index])
                return

    ###################################################################################
    def focus_prev(self) -> None:
        """Move focus to prev widget"""
        focussed_widget = self.which_widget_has_focus()
        children = list(self.children_widgets())
        if not focussed_widget:
            focussed_widget = children[0]

        # Which child has focus
        next_widget_index = -1
        for num, widget in enumerate(children):
            if widget == focussed_widget:
                next_widget_index = num

        while True:
            next_widget_index = (next_widget_index + (len(children) - 1)) % len(
                children
            )
            if children[next_widget_index].focusable:
                self.focus_on_widget(children[next_widget_index])
                return


# EOF
