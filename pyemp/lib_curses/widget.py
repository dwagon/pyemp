"""Parent class for widgets"""

import curses
from enum import StrEnum, auto
from collections import namedtuple
from typing import Callable, Any, Self, Optional
from .mouse_events import MouseEvent
from .exceptions import ScreenTooSmall
from .keys import Keys

Dimension = namedtuple("Dimension", "nlines ncols begin_y begin_x ")


#######################################################################################
class BindingName(StrEnum):
    """Event Binding names"""

    ON_FOCUS = auto()
    LOSE_FOCUS = auto()


#######################################################################################
#######################################################################################
#######################################################################################
class Widget:
    """Generic Widget Class"""

    _window_list = []

    def __init__(self, **kwargs: Any):
        self.begin_y = kwargs.get("begin_y", 0)
        self.begin_x = kwargs.get("begin_x", 0)
        self.nlines: Optional[int] = kwargs.get("nlines", None)
        self.ncols: Optional[int] = kwargs.get("ncols", None)
        self.border = kwargs.get("border", False)
        self.name = kwargs.get("name", "")
        self.focus = kwargs.get("focus", False)
        self.focusable = kwargs.get("focusable", True)
        self.bindings: dict[Keys, Callable[[], None]] = kwargs.get("bindings", {})
        self.mouse_bindings: dict[MouseEvent, Callable[[int, int], None]] = {}
        self.misc_bindings: dict[BindingName, Optional[Callable[[], None]]] = {
            BindingName.ON_FOCUS: kwargs.get("onfocus"),
            BindingName.LOSE_FOCUS: kwargs.get("loosefocus"),
        }
        self._parent = None
        self._window = None
        self._border_window = None

    ###################################################################################
    def debug(self, msg: str):
        """Debug log"""
        with open("/tmp/widget_err", "a", encoding="utf-8") as outfh:
            outfh.write(f"{msg}\n")

    ###################################################################################
    def onFocus(self):
        """This widget has received focus"""
        if self.misc_bindings[BindingName.ON_FOCUS]:
            self.misc_bindings[BindingName.ON_FOCUS]()

    ###################################################################################
    def loseFocus(self):
        """This widget has lost focus"""
        if self.misc_bindings[BindingName.LOSE_FOCUS]:
            self.misc_bindings[BindingName.LOSE_FOCUS]()

    ###################################################################################
    def draw(self) -> None:
        """Draw the Widget"""
        if self._border_window:
            self._border_window.border()

    ###################################################################################
    @property
    def height(self) -> int:
        """height of widget"""
        return self.nlines

    ###################################################################################
    @property
    def width(self) -> int:
        """width of widget"""
        return self.ncols

    ###################################################################################
    def layout(self) -> None:
        """Create the curses implementation of the widget
        Happens after object creation and before drawing for the first time"""
        if self.border:
            self.layout_border_window()
            # self.begin_y += 1  # Offset the subwindow by the size of the border
            # self.begin_x += 1
        dimension = Dimension(self.nlines, self.ncols, self.begin_y, self.begin_x)

        win_size = self.calc_window_size(dimension, border_win=False)

        if self._border_window:
            self.debug(
                f"{self.name} border = derwin({win_size.nlines}, {win_size.ncols}, 1, 1)"
            )
            self._window = self._border_window.derwin(
                win_size.nlines, win_size.ncols, 1, 1
            )
        else:
            self._window = self._parent.derwin(
                win_size.nlines, win_size.ncols, win_size.begin_y, win_size.begin_x
            )
        self._window_list.append([self.name, win_size, self._window])

    ###################################################################################
    def layout_border_window(self):
        """If there is a border then lay it out as a new window"""
        dimension = Dimension(self.nlines, self.ncols, self.begin_y, self.begin_x)
        win_size = self.calc_window_size(dimension, border_win=True)
        self._border_window = self._parent.derwin(
            win_size.nlines, win_size.ncols, win_size.begin_y, win_size.begin_x
        )
        self._window_list.append([self.name + " border", win_size, self._border_window])

    ###################################################################################
    def calc_window_size(self, dimension: Dimension, border_win=False) -> Dimension:
        """How big the inner canvas should be based on the borders"""

        nlines, ncols, begin_y, begin_x = dimension
        nlines = self.calculate_height(dimension, border_win)
        ncols = self.calculate_width(dimension, border_win)
        ans = Dimension(nlines, ncols, begin_y, begin_x)
        self.debug(f"{self.name} calc_w_s({dimension}, {border_win}) {ans=}")
        return ans

    ###################################################################################
    def calculate_height(self, requested: Dimension, border_win: bool = False) -> int:
        """Height to use"""
        max_height = self.avail_height()
        max_height -= requested.begin_y
        if requested.nlines is None:
            nlines = max_height
        else:
            nlines = requested.nlines
        if self.border and not border_win:  # Leave room for border
            nlines -= 2
        if nlines > max_height:
            raise ScreenTooSmall(self.name + " height", nlines, max_height)
        return nlines

    ###################################################################################
    def calculate_width(self, requested: Dimension, border_win: bool = False) -> int:
        """Width to use"""
        max_width = self.avail_width()
        max_width -= requested.begin_x

        if requested.ncols is None:
            ncols = max_width
        else:
            ncols = requested.ncols

        if self.border and not border_win:
            ncols -= 2
        if ncols > max_width:
            raise ScreenTooSmall(self.name + " width", ncols, max_width)
        return ncols

    ###################################################################################
    def avail_width(self) -> int:
        """How much width do we have available"""
        _, max_width = self._parent.getmaxyx()
        return max_width

    ###################################################################################
    def avail_height(self) -> int:
        """How much width do we have available"""
        max_height, _ = self._parent.getmaxyx()
        return max_height

    ###################################################################################
    def handle_input(self, key: Keys) -> None:
        """Handle character input"""
        self.debug(f"\t{self.name} {self.bindings=}")
        if key in self.bindings:
            self.debug(f"\t{self.name} handle_input({key=})")
            return self.bindings[key]()
        return None

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
