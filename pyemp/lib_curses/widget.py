"""Parent class for widgets"""

import curses
from typing import Callable, Any
from ..misc import debug
from .mouse_events import MouseEvent


#######################################################################################
#######################################################################################
#######################################################################################
class Widget:
    """Generic Widget Class"""

    def __init__(self, **kwargs: Any):
        self.begin_y = kwargs.get("begin_y")
        self.begin_x = kwargs.get("begin_x")
        self.root = kwargs.get("root")
        self.parent = kwargs.get("parent")
        if not self.root:
            self.root = self.parent
        self.bindings: dict[Any, Callable[[], None]] = {}
        self.mouse_bindings: dict[MouseEvent, Callable[[int, int], None]] = {}

    def draw(self) -> None:
        """Draw the Widget"""
        raise NotImplementedError

    def handle_input(self, key: int) -> None:
        """Handle character input"""
        if key in self.bindings:
            return self.bindings[key]()
        return None

    def handle_mouse(self) -> None:
        """Hande mouse input"""
        # mouse event, represented as a 5-tuple (id, x, y, z, bstate)
        if not self.mouse_bindings:
            return None
        mouse_event = curses.getmouse()
        debug(f"{self} {mouse_event=}")
        _, x, y, _, _ = mouse_event
        if self.in_window(x, y):
            for binding, callback in self.mouse_bindings.items():
                debug(f"{binding=} {callback=}")
                if binding & mouse_event[4]:
                    debug(f"{self} mouse {mouse_event=}")
                    return callback(mouse_event[1], mouse_event[2])
        curses.ungetmouse(
            mouse_event[0],
            mouse_event[1],
            mouse_event[2],
            mouse_event[3],
            mouse_event[4],
        )
        return None

    def in_window(self, x: int, y: int) -> bool:
        """Return if x,y is in this window"""
        y1, x1 = self.window.getbegyx()
        y2, x2 = self.window.getmaxyx()
        return x1 < x < x2 and y1 < y < y2

    def has_finished(self) -> bool:
        """Has the widget finished doing its thing"""
        return False


# EOF
