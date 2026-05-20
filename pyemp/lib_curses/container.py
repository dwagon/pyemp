"""Modal Curses Popup"""

from typing import Any

from .widget import Widget
from .keys import Keys


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
            widget.draw()

    ###################################################################################
    def handle_input(self, key: Keys) -> None:
        """Handle character input"""
        self.debug(f"{self.name} {self.bindings}")
        for widget in self._widgets:
            widget.handle_input(key)

        if key in self.bindings:
            self.debug(f"{self.name} handle_input({key=})")
            return self.bindings[key]()
        return None


# EOF
