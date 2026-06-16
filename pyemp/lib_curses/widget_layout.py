"""Class containing all the layout code for widgets"""

import curses
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

        # Leave a user defined bit of space around the edge
        self.pad = kwargs.get("pad", 0)  # All over padding
        self.pad_top = kwargs.get("pad_top", self.pad)
        self.pad_bottom = kwargs.get("pad_bottom", self.pad)
        self.pad_left = kwargs.get("pad_left", self.pad)
        self.pad_right = kwargs.get("pad_right", self.pad)

        self.height: Optional[int] = kwargs.get("height", None)
        self.width: Optional[int] = kwargs.get("width", None)
        self.border = kwargs.get("border", False)
        self.debugFlag = kwargs.get("debug", False)
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
        begin_x = 0
        begin_y = 0
        if self._border_window:
            begin_y = 1
            begin_x = 1
        else:
            begin_x = self.begin_x
            begin_y = self.begin_y
        requested_size = Dimension(self.height, self.width, begin_y, begin_x)
        size = self.calc_window_size(requested_size, border_win=False)

        if self._border_window:
            parent_win = self._border_window
        else:
            parent_win = self._parent_window
        self.debug(
            f"derwin(height={size.height}, width={size.width}, "
            f"begin_y={size.begin_y}, begin_x={size.begin_x})"
        )
        self._window = parent_win.derwin(
            size.height, size.width, size.begin_y, size.begin_x
        )
        self.width = size.width
        self.height = size.height
        self.debug(f"Setting {self.width=} and {self.height=}")

    ###################################################################################
    def layout_border_window(self):
        """If there is a border then lay it out as a new window"""
        size = Dimension(self.height, self.width, self.begin_y, self.begin_x)

        win_size = self.calc_window_size(size, border_win=True)
        self.debug(
            f"border(height={win_size.height}, width={win_size.width}, "
            f"begin_y={win_size.begin_y}, begin_x={win_size.begin_x})"
        )
        self._border_window = self._parent_window.derwin(
            win_size.height, win_size.width, win_size.begin_y, win_size.begin_x
        )

    ###################################################################################
    def calc_window_size(self, dimension: Dimension, border_win=False) -> Dimension:
        """How big the inner canvas should be based on the borders"""
        self.debug(f"calc_window_size({dimension})")
        height, width, begin_y, begin_x = dimension
        if border_win and not self._border_window:
            begin_y += self.pad_top
            begin_x += self.pad_left
        height = self.calculate_height(dimension, border_win)
        width = self.calculate_width(dimension, border_win)
        ans = Dimension(height, width, begin_y, begin_x)
        self.debug(f"calc_window_size() = {ans}", force=True)
        return ans

    ###################################################################################
    def calculate_height(self, requested: Dimension, border_win: bool = False) -> int:
        """Height to use"""
        if requested.height:
            height = requested.height
            if self.border and not border_win:
                height -= 2
            self.debug(f"calc_height() {height=}")
            return height
        max_h = self.avail_height() - requested.begin_y - self.pad_top - self.pad_bottom
        min_h = self.required_height + self.pad_top + self.pad_bottom
        if self.border and not border_win:
            max_h -= 2
        if self.border and border_win:
            min_h += 2
        height = max_h if self.fit == FitType.MAX_FIT else min_h
        self.debug(f"calc_height() {requested=} {min_h=} {max_h=} {height=}")
        return height

    ###################################################################################
    def calculate_width(self, requested: Dimension, border_win: bool = False) -> int:
        """Width to use"""
        if requested.width:
            width = requested.width
            if self.border and not border_win:
                width -= 2
                self.debug(f"calc_width() {width=}")
            return width
        max_w = self.avail_width() - requested.begin_x - self.pad_left - self.pad_right
        min_w = self.required_width + self.pad_left + self.pad_right
        if self.border and not border_win:
            max_w -= 2
        if self.border and border_win:
            min_w += 2
        width = max_w if self.fit == FitType.MAX_FIT else min_w
        self.debug(
            f"calc_width() req={requested.width} {min_w=} {max_w=} {self.fit=} {width=}"
        )

        return width

    ###################################################################################
    def avail_width(self) -> int:
        """How much width do we have available"""
        if self._parent_window:
            _, max_width = self._parent_window.getmaxyx()
        else:
            max_width = curses.COLS
        return max_width

    ###################################################################################
    def avail_height(self) -> int:
        """How much height do we have available"""
        if self._parent_window:
            max_height, _ = self._parent_window.getmaxyx()
        else:
            max_height = curses.LINES
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

    ###################################################################################
    def debug(self, msg: str, force: bool = False):
        """Debug log"""
        if not self.debugFlag and not force:
            return
        with open("/tmp/widget_err", "a", encoding="utf-8") as outfh:
            outfh.write(f"{repr(self)}: {msg}\n")


# EOF
