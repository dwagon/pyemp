"""Container of other widgets"""

import curses
from typing import Any, Optional

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
        self._widgets: list[Widget] = []

    ###################################################################################
    def layout(self):
        """Setup - outer canvas for borders,etc, inner canvas for widgets"""
        super().layout()
        for widget in self._widgets:
            widget.set_parent(self._window)
            widget.layout()

    ###################################################################################
    def add(self, widget: Widget, name: str = "") -> Widget:
        """Add a widget to the container"""
        if not name:
            name = widget.assign_name()
        self._widgets.append(widget)
        widget.name = name
        widget.parent_widget = self
        return widget

    ###################################################################################
    def delete(self, name: str):
        """Remove a widget from the container"""
        for widget in self._widgets:
            if widget.name == name:
                self._widgets.remove(widget)

    ###################################################################################
    @property
    def required_height(self) -> int:
        """required_height of container"""
        if self._widgets:
            h = max(_.required_height for _ in self._widgets)
        else:
            h = 1  # Min size
        self.debug(f"required_height={h}")
        return h

    ###################################################################################
    @property
    def required_width(self) -> int:
        """required_width of container"""
        if self._widgets:
            w = max(_.required_width for _ in self._widgets)
        else:
            w = 1  # Min size
        self.debug(f"required_width={w}")

        return w

    ###################################################################################
    def draw(self):
        """Draw the window"""
        super().draw()
        for widget in self._widgets:
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
    def focus_widget(self, focus_on_widget: Widget) -> None:
        """Set focus on specific widget"""
        for widget in self._widgets:
            if widget.focus:
                widget.loseFocus()
            widget.focus = False
        focus_on_widget.focus = True
        focus_on_widget.gainFocus()

    ###################################################################################
    def which_widget_has_focus(self) -> Optional[Widget]:
        """Which widget has focus"""
        for widget in self._widgets:
            if widget.focus:
                return widget
        return None

    ###################################################################################
    def focus_next(self) -> None:
        """Move focus to next widget"""
        widget = self.which_widget_has_focus()
        if not widget:
            return
        index = self._widgets.index(widget)
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
        widget = self.which_widget_has_focus()
        if not widget:
            return
        index = self._widgets.index(widget)
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


# EOF
