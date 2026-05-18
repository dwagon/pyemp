"""Parent class for widgets"""

import curses
from collections import namedtuple
from typing import Callable, Any, Self, Optional
from .mouse_events import MouseEvent
from .exceptions import ScreenTooSmall

Dimension = namedtuple("Dimension", "nlines ncols begin_y begin_x ")


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
        self.bindings: dict[Any, Callable[[], None]] = kwargs.get("bindings", {})
        self.mouse_bindings: dict[MouseEvent, Callable[[int, int], None]] = {}
        self.parent = None
        self.window = None
        self.border_window = None
        self.name = kwargs.get("name", "")

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
        self.debug(f"{self} height={self.nlines}")
        return self.nlines

    ###################################################################################
    @property
    def width(self) -> int:
        """width of widget"""
        self.debug(f"{self} width={self.ncols}")
        return self.ncols

    ###################################################################################
    def layout(self) -> None:
        """Create the curses implementation of the widget
        Happens after object creation and before drawing for the first time"""
        self.debug(f"{self} layout")
        if self.border:
            self.layout_border_window()
            # self.begin_y += 1  # Offset the subwindow by the size of the border
            # self.begin_x += 1
        dimension = Dimension(self.nlines, self.ncols, self.begin_y, self.begin_x)

        win_size = self.calc_window_size(dimension, border_win=False)

        self.debug(
            f"{self.name} derwin({win_size.nlines}, {win_size.ncols}, {win_size.begin_y}, {win_size.begin_x})"
        )
        if self.border_window:
            self.window = self.border_window.derwin(
                win_size.nlines, win_size.ncols, 1, 1
            )
        else:
            self.window = self.parent.derwin(
                win_size.nlines, win_size.ncols, win_size.begin_y, win_size.begin_x
            )
        self._window_list.append([self.name, win_size, self.window])
        self.debug(f"{self} layout over")

    ###################################################################################
    def layout_border_window(self):
        """If there is a border then lay it out as a new window"""
        dimension = Dimension(self.nlines, self.ncols, self.begin_y, self.begin_x)
        win_size = self.calc_window_size(dimension, border_win=True)
        self.debug(
            f"{self.name} border derwin = ({win_size.nlines}, {win_size.ncols}, {win_size.begin_y}, {win_size.begin_x})"
        )
        self.border_window = self.parent.derwin(
            win_size.nlines, win_size.ncols, win_size.begin_y, win_size.begin_x
        )
        self._window_list.append([self.name + " border", win_size, self.border_window])

    ###################################################################################
    def calc_window_size(self, dimension: Dimension, border_win=False) -> Dimension:
        """How big the inner canvas should be based on the borders"""

        nlines, ncols, begin_y, begin_x = dimension
        self.debug(f"{self} calc_window_size({dimension}, {border_win=})")
        nlines = self.calculate_height(dimension, border_win)
        ncols = self.calculate_width(dimension, border_win)
        ans = Dimension(nlines, ncols, begin_y, begin_x)
        self.debug(f"{self} calc_window_size() {ans}")
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
        self.debug(
            f"{self} calculate_height({requested}, {max_height=}, {border_win=}) -> {nlines}"
        )
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
        self.debug(
            f"{self} calculate_width({requested}, {max_width=}, {border_win=}) -> {ncols}"
        )
        if ncols > max_width:
            raise ScreenTooSmall(self.name + " width", ncols, max_width)
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
            self.debug("Window List")
            for name, dimension, window in self._window_list:  # debug
                self.debug(f"\t{name} {dimension} {window.getbegyx()}")
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
