"""Parent class for widgets"""

import curses
from enum import StrEnum, Enum, auto
from collections import namedtuple
from typing import Callable, Any, Self, Optional
from .mouse_events import MouseEvent
from .keys import Keys

Dimension = namedtuple("Dimension", "height width begin_y begin_x ")


#######################################################################################
class FitType(Enum):
    """How to fit a widget"""

    MIN_FIT = auto()
    MAX_FIT = auto()


#######################################################################################
class BindingName(StrEnum):
    """Event Binding names"""

    GAIN_FOCUS = auto()
    LOSE_FOCUS = auto()


#######################################################################################
#######################################################################################
#######################################################################################
class Widget:
    """Generic Widget Class"""

    def __init__(self, **kwargs: Any):
        self.begin_y = kwargs.get("begin_y", 0)
        self.begin_x = kwargs.get("begin_x", 0)
        self.height: Optional[int] = kwargs.get("height", None)
        self.width: Optional[int] = kwargs.get("width", None)
        self.border = kwargs.get("border", False)
        self.name = kwargs.get("name", "")
        self.focus = False
        self.focusable = kwargs.get("focusable", True)
        self.bindings: dict[Keys, Callable[[], None]] = kwargs.get("bindings", {})
        self.mouse_bindings: dict[MouseEvent, Callable[[int, int], None]] = {}
        self.misc_bindings: dict[BindingName, Optional[Callable[[], None]]] = {
            BindingName.GAIN_FOCUS: kwargs.get("gainfocus"),
            BindingName.LOSE_FOCUS: kwargs.get("loosefocus"),
        }
        self.fit = kwargs.get("fit", FitType.MAX_FIT)
        self._parent = None
        self._window = None
        self._border_window = None

    ###################################################################################
    def debug(self, msg: str):
        """Debug log"""
        with open("/tmp/widget_err", "a", encoding="utf-8") as outfh:
            outfh.write(f"{repr(self)}: {msg}\n")

    ###################################################################################
    def gainFocus(self):
        """This widget has received focus"""
        if self.misc_bindings[BindingName.GAIN_FOCUS]:
            self.misc_bindings[BindingName.GAIN_FOCUS]()

    ###################################################################################
    def loseFocus(self):
        """This widget has lost focus"""
        if self.misc_bindings[BindingName.LOSE_FOCUS]:
            self.misc_bindings[BindingName.LOSE_FOCUS]()

    ###################################################################################
    def draw(self) -> None:
        """Draw the Widget"""
        if self.focus:
            self._window.attron(curses.A_BOLD)
        else:
            self._window.attroff(curses.A_BOLD)
        if self._border_window:
            if self.focus:
                self._border_window.border(0, 0, 0, 0, "*")
            else:
                self._border_window.border()

    ###################################################################################
    @property
    def required_height(self) -> int:
        """required_height of widget"""
        raise NotImplementedError

    ###################################################################################
    @property
    def required_width(self) -> int:
        """required_width of widget"""
        raise NotImplementedError

    ###################################################################################
    def layout(self) -> None:
        """Create the curses implementation of the widget
        Happens after object creation and before drawing for the first time"""
        if self.border:
            self.layout_border_window()
        self.layout_window()

    ###################################################################################
    def layout_window(self) -> None:
        """Layout the non-border window"""
        begin_x = self.begin_x
        begin_y = self.begin_y
        if self._border_window:
            begin_y = 1
            begin_x = 1
        req_size = Dimension(self.height, self.width, begin_y, begin_x)
        size = self.calc_window_size(req_size, border_win=False)

        if self._border_window:
            self.debug(
                f"derwinA({size.height}, {size.width}, {size.begin_y}, {size.begin_x})"
            )
            self._window = self._border_window.derwin(
                size.height, size.width, size.begin_y, size.begin_x
            )
        else:
            self.debug(
                f"derwinB({size.height}, {size.width}, {size.begin_y}, {size.begin_x})"
            )
            self._window = self._parent.derwin(
                size.height, size.width, size.begin_y, size.begin_x
            )

    ###################################################################################
    def layout_border_window(self):
        """If there is a border then lay it out as a new window"""
        size = Dimension(self.height, self.width, self.begin_y, self.begin_x)
        win_size = self.calc_window_size(size, border_win=True)
        self.debug(
            f"border derwin({win_size.height}, {win_size.width}, "
            f"{win_size.begin_y}, {win_size.begin_x})"
        )
        self._border_window = self._parent.derwin(
            win_size.height, win_size.width, win_size.begin_y, win_size.begin_x
        )

    ###################################################################################
    def calc_window_size(self, dimension: Dimension, border_win=False) -> Dimension:
        """How big the inner canvas should be based on the borders"""

        height, width, begin_y, begin_x = dimension
        height = self.calculate_height(dimension, border_win)
        width = self.calculate_width(dimension, border_win)
        ans = Dimension(height, width, begin_y, begin_x)
        return ans

    ###################################################################################
    def calculate_height(self, requested: Dimension, border_win: bool = False) -> int:
        """Height to use"""
        max_h = self.avail_height()
        max_h -= requested.begin_y
        min_h = self.required_height
        if self.border:
            if border_win:
                min_h += 2
            else:
                max_h -= 2
        if requested.height is None:
            height = max_h if self.fit == FitType.MAX_FIT else min_h
        else:
            height = requested.height
        height = min_h if height < min_h else height
        height = max_h if height > max_h else height
        self.debug(f"calculate_height() {min_h=} {max_h=} {height=}")
        return height

    ###################################################################################
    def calculate_width(self, requested: Dimension, border_win: bool = False) -> int:
        """Width to use"""
        max_w = self.avail_width()
        max_w -= requested.begin_x
        min_w = self.required_width
        if self.border:
            if border_win:
                min_w += 2
            else:
                max_w -= 2

        if requested.width is None:
            width = max_w if self.fit == FitType.MAX_FIT else min_w
        else:
            width = requested.width

        width = min_w if width < min_w else width
        width = max_w if width > max_w else width
        self.debug(f"calculate_width() {min_w=} {max_w=} {width=}")

        return width

    ###################################################################################
    def avail_width(self) -> int:
        """How much width do we have available"""
        _, max_width = self._parent.getmaxyx()
        return max_width

    ###################################################################################
    def avail_height(self) -> int:
        """How much height do we have available"""
        max_height, _ = self._parent.getmaxyx()
        return max_height

    ###################################################################################
    def handle_input(self, key: Keys) -> bool:
        """Handle character input - return if event handled"""
        self.debug(f"\t{self.bindings=}")
        if key in self.bindings:
            self.debug(f"\thandle_input({key=})")
            self.bindings[key]()
            return True
        return False

    ###################################################################################
    def assign_name(self) -> str:
        """Assign a name if one isn't given"""
        return self.__class__.__name__

    ###################################################################################
    def add(self, widget: Self, name: str = "") -> Widget:
        """Add a subwidget - for containers"""
        raise AttributeError("Only containers can add subwidgets")

    ###################################################################################
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"

    ###################################################################################
    def set_parent(self, window: curses.window):
        """Set the parent"""
        self._parent = window

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
        y1, x1 = self._window.getbegyx()
        y2, x2 = self._window.getmaxyx()
        return x1 < x < x2 and y1 < y < y2


# EOF
