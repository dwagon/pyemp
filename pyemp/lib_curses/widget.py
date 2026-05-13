"""Parent class for widgets"""

import curses
from typing import Callable, Any, Self
from .mouse_events import MouseEvent


#######################################################################################
#######################################################################################
#######################################################################################
class Widget:
    """Generic Widget Class"""

    def __init__(self, **kwargs: Any):
        self.begin_y = kwargs.get("begin_y", 0)
        self.begin_x = kwargs.get("begin_x", 0)
        self.parent = kwargs.get("parent")
        self.bindings: dict[Any, Callable[[], None]] = kwargs.get("bindings", {})
        self.mouse_bindings: dict[MouseEvent, Callable[[int, int], None]] = {}
        self.name = ""

    ###################################################################################
    def draw(self) -> None:
        """Draw the Widget"""
        raise NotImplementedError

    ###################################################################################
    def layout(self) -> None:
        """Create the curses implementation of the widget
        Happens after object creation and before drawing for the first time"""

    ###################################################################################
    def handle_input(self, key: int) -> None:
        """Handle character input"""
        if key in self.bindings:
            return self.bindings[key]()
        return None

    ###################################################################################
    def add(self, name: str, widget: Self):
        """Add a subwidget - for containers"""
        raise AttributeError("Only containers can add subwidgets")

    ###################################################################################
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"

    ###################################################################################
    def handle_mouse(self) -> None:
        """Hande mouse input"""
        # mouse event, represented as a 5-tuple (id, x, y, z, bstate)
        if not self.mouse_bindings:
            return None
        mouse_event = curses.getmouse()
        _, x, y, _, _ = mouse_event
        if self.in_window(x, y):
            for binding, callback in self.mouse_bindings.items():
                if binding & mouse_event[4]:
                    return callback(mouse_event[1], mouse_event[2])
        curses.ungetmouse(
            mouse_event[0],
            mouse_event[1],
            mouse_event[2],
            mouse_event[3],
            mouse_event[4],
        )
        return None

    ###################################################################################
    def in_window(self, x: int, y: int) -> bool:
        """Return if x,y is in this window"""
        y1, x1 = self.window.getbegyx()
        y2, x2 = self.window.getmaxyx()
        return x1 < x < x2 and y1 < y < y2


# EOF
