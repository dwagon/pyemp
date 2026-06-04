"""Class containing all the layout code for widgets"""

from collections import namedtuple
from typing import Any, Optional
from enum import Enum, auto

Dimension = namedtuple("Dimension", "height width begin_y begin_x ")


#######################################################################################
class FitType(Enum):
    """How to fit a widget"""

    MIN_FIT = auto()
    MAX_FIT = auto()


#######################################################################################
#######################################################################################
#######################################################################################
class WidgetLayout:
    """Widget Layout Code to simplify Widget code"""

    ###################################################################################
    def __init__(self, **kwargs: Any):
        self._laid_out = False
        self.begin_y = kwargs.get("begin_y", 0)
        self.begin_x = kwargs.get("begin_x", 0)
        self.height: Optional[int] = kwargs.get("height", None)
        self.width: Optional[int] = kwargs.get("width", None)
        self.border = kwargs.get("border", False)
        self.fit = kwargs.get("fit", FitType.MAX_FIT)

        self._parent_window = None
        self._window = None
        self._border_window = None

    ###################################################################################
    def layout(self) -> None:
        """Create the curses implementation of the widget
        Happens after object creation and before drawing for the first time"""
        if self._laid_out:
            return
        if self.border:
            self.layout_border_window()
        self.layout_window()
        self._laid_out = True

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
            # self.debug(
            #     f"derwinA(height={size.height}, width={size.width}, "
            #     f"begin_y={size.begin_y}, begin_x={size.begin_x})"
            # )
            self._window = self._border_window.derwin(
                size.height, size.width, size.begin_y, size.begin_x
            )
        else:
            # self.debug(
            #     f"derwinB(height={size.height}, width={size.width}, "
            #     f"begin_y={size.begin_y}, begin_x={size.begin_x})"
            # )
            self._window = self._parent_window.derwin(
                size.height, size.width, size.begin_y, size.begin_x
            )

    ###################################################################################
    def layout_border_window(self):
        """If there is a border then lay it out as a new window"""
        size = Dimension(self.height, self.width, self.begin_y, self.begin_x)
        win_size = self.calc_window_size(size, border_win=True)
        # self.debug(
        #     f"border(height={win_size.height}, width={win_size.width}, "
        #     f"begin_y={win_size.begin_y}, begin_x={win_size.begin_x})"
        # )
        self._border_window = self._parent_window.derwin(
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
        if self.border and border_win:
            min_h += 2
        if requested.height is None:
            height = max_h if self.fit == FitType.MAX_FIT else min_h
        else:
            height = requested.height
            height += 2 if border_win else 0
        height = min_h if height < min_h else height
        # height = max_h if height > max_h else height
        # self.debug(f"calc_height() {min_h=} {max_h=} {height=}")
        return height

    ###################################################################################
    def calculate_width(self, requested: Dimension, border_win: bool = False) -> int:
        """Width to use"""
        max_w = self.avail_width()
        max_w -= requested.begin_x
        min_w = self.required_width
        if self.border and border_win:
            min_w += 2
        if requested.width is None:
            width = max_w if self.fit == FitType.MAX_FIT else min_w
        else:
            width = requested.width
            width += 2 if border_win else 0
        width = min_w if width < min_w else width
        width = max_w if width > max_w else width
        # self.debug(
        #     f"calc_width() req={requested.width} {min_w=} {max_w=} {self.fit=} {width=}"
        # )

        return width

    ###################################################################################
    def avail_width(self) -> int:
        """How much width do we have available"""
        _, max_width = self._parent_window.getmaxyx()
        return max_width

    ###################################################################################
    def avail_height(self) -> int:
        """How much height do we have available"""
        max_height, _ = self._parent_window.getmaxyx()
        return max_height

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


# EOF
