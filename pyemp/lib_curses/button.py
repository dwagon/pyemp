"""Curses based button"""

import curses
from typing import Optional, Callable, Any

from .keys import Keys
from .mouse_events import MouseEvent
from .widget import Widget, FitType


#######################################################################################
#######################################################################################
#######################################################################################
class Button(Widget):
    """Button Widget"""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.label = kwargs["label"]
        self.value = kwargs.get("value", self.label)
        self.callback: Optional[Callable[[], None]] = kwargs.get("callback", None)
        self.border: bool = kwargs.get("border", True)
        self.selected = kwargs.get("selected", False)
        self.mouse_bindings = {
            MouseEvent.BUTTON1_CLICKED: self.clicked,
            MouseEvent.BUTTON1_PRESSED: self.clicked,
            MouseEvent.BUTTON1_DOUBLE_CLICKED: self.clicked,
        }
        self.bindings = {Keys.KEY_ENTER: self.pressed, Keys.KEY_RETURN: self.pressed}
        self.fit = FitType.MIN_FIT

    ###################################################################################
    def draw(self):
        """Draw the button"""
        super().draw()
        if self.selected:
            self._window.attron(curses.A_REVERSE)
        else:
            self._window.attroff(curses.A_REVERSE)
        self._window.addstr(0, 0, self.label)

    ###################################################################################
    def clicked(self, x: int, y: int, bstate: int) -> None:
        """Mouse has clicked on the button"""
        _ = (x, y, bstate)  # Prevent unused arg complaint
        self.pressed()

    ###################################################################################
    def pressed(self):
        """Button has been pressed / selected"""
        self.selected = not self.selected
        # Tell parent (if buttonbox) that we were pressed
        if hasattr(self.widget_tree.parent(self.node_id).data, "button_pressed"):
            self.widget_tree.parent(self.node_id).data.button_pressed(self)
        if self.callback:
            self.callback()

    ###################################################################################
    @property
    def required_width(self) -> int:
        """Width of the button (extra one because curses seems to not handle one char wide"""
        return len(self.label) + 1

    ###################################################################################
    @property
    def required_height(self) -> int:
        """Height of the button"""
        return 1

    ###################################################################################
    def assig_name(self) -> str:
        """Assign a name if one isn't given"""
        return f"Button {self.label}"

    ###################################################################################
    def __repr__(self):
        return f"<Button {self.label}>"


# EOF
