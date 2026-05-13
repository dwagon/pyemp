"""Parent class for widgets"""

import curses
from collections import namedtuple
from typing import Callable, Any, Self
from .mouse_events import MouseEvent
from .exceptions import ScreenTooSmall

Dimension = namedtuple("Dimensions", "nlines ncols begin_y begin_x")


#######################################################################################
#######################################################################################
#######################################################################################
class Widget:
    """Generic Widget Class"""

    def __init__(self, **kwargs: Any):
        self.begin_y = kwargs.get("begin_y", 0)
        self.begin_x = kwargs.get("begin_x", 0)
        self.nlines: int = kwargs.get("nlines", -1)
        self.ncols: int = kwargs.get("ncols", -1)
        self.border = kwargs.get("border", False)
        self.bindings: dict[Any, Callable[[], None]] = kwargs.get("bindings", {})
        self.mouse_bindings: dict[MouseEvent, Callable[[int, int], None]] = {}
        self.parent = None
        self.window = None
        self.border_window = None
        self.name = ""

    ###################################################################################
    def debug(self, msg: str):
        """Debug log"""
        with open("/tmp/widget_err", "a", encoding="utf-8") as outfh:
            outfh.write(f"{msg}\n")

    ###################################################################################
    def draw(self) -> None:
        """Draw the Widget"""
        if self.border_window:
            self.border_window.border()

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
        dimension = Dimension(self.nlines, self.ncols, self.begin_y, self.begin_x)

        nlines, ncols, begin_y, begin_x = self.calc_window_size(
            dimension, border_win=False
        )
        self.window = self.parent.derwin(nlines, ncols, begin_y, begin_x)

    ###################################################################################
    def layout_border_window(self):
        """If there is a border then lay it out as a new window"""
        dimension = Dimension(self.nlines, self.ncols, self.begin_y, self.begin_x)

        b_nlines, b_ncols, b_begin_y, b_begin_x = self.calc_window_size(
            dimension, border_win=True
        )

        self.border_window = self.parent.derwin(b_nlines, b_ncols, b_begin_y, b_begin_x)

    ###################################################################################
    def calc_window_size(self, dimension: Dimension, border_win=False) -> Dimension:
        """How big the inner canvas should be based on the borders"""

        nlines, ncols, begin_y, begin_x = dimension
        nlines = self.calculate_height(border_win)
        ncols = self.calculate_width(border_win)

        if not border_win and self.border:
            begin_y += 1
            begin_x += 1

        return Dimension(nlines, ncols, begin_y, begin_x)

    ###################################################################################
    def calculate_height(self, border_win: bool = False) -> int:
        """Height to use"""
        requested = self.height
        nrows = requested
        max_height = self.avail_height()
        if border_win:
            nrows += 2
        if nrows < 0:
            nrows = max_height
        if nrows > max_height:
            raise ScreenTooSmall(self.name + " height", requested, max_height)
        return nrows

    ###################################################################################
    def calculate_width(self, border_win: bool = False) -> int:
        """Width to use"""
        requested = self.width
        ncols = requested
        max_width = self.avail_width()
        if border_win:
            ncols += 2
        if ncols < 0:
            ncols = max_width
        if ncols > max_width:
            raise ScreenTooSmall(self.name + " width", requested, max_width)
        return ncols

    ###################################################################################
    def avail_width(self) -> int:
        """How much width do we have available"""
        _, max_width = self.parent.getmaxyx()
        return max_width

    ###################################################################################
    def avail_height(self) -> int:
        """How much width do we have available"""
        max_height, _ = self.parent.getmaxyx()
        return max_height

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
