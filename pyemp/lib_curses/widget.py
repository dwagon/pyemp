"""Parent class for widgets"""

import curses
from collections import namedtuple
from enum import StrEnum, Enum, auto
from typing import Callable, Any, Self, Optional

import treelib

from .keys import Keys
from .mouse_events import MouseEvent

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
        self.fit = kwargs.get("fit", FitType.MAX_FIT)
        self.focusable = kwargs.get("focusable", True)
        self.focus = False
        self.root_ui = None
        self.node_id = ""
        self._laid_out = False
        self.bindings: dict[Keys, Callable[[], None]] = kwargs.get("bindings", {})
        self.mouse_bindings: dict[MouseEvent, Callable[[int, int, int], None]] = {}
        self.misc_bindings: dict[BindingName, Optional[Callable[[], None]]] = {
            BindingName.GAIN_FOCUS: kwargs.get("gainfocus"),
            BindingName.LOSE_FOCUS: kwargs.get("loosefocus"),
        }
        self._parent_window = None
        self._window = None
        self._border_window = None

    ###################################################################################
    @property
    def widget_tree(self) -> treelib.Tree:
        """Shortcut to the widget tree"""
        return self.root_ui.widget_tree

    ###################################################################################
    def debug(self, msg: str):
        """Debug log"""
        with open("/tmp/widget_err", "a", encoding="utf-8") as outfh:
            outfh.write(f"{repr(self)}: {msg}\n")

    ###################################################################################
    def enclose(self, y: int, x: int) -> bool:
        """Is the coord in our window?"""
        return self._window.enclose(y, x)

    ###################################################################################
    def gainFocus(self):
        """This widget has received focus"""
        self.debug("Gained focus")
        if self.misc_bindings[BindingName.GAIN_FOCUS]:
            self.misc_bindings[BindingName.GAIN_FOCUS]()

    ###################################################################################
    def loseFocus(self):
        """This widget has lost focus"""
        self.debug("Lost Focus")
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
            #     f"derwinA({size.height}, {size.width}, {size.begin_y}, {size.begin_x})"
            # )
            self._window = self._border_window.derwin(
                size.height, size.width, size.begin_y, size.begin_x
            )
        else:
            # self.debug(
            #     f"derwinB({size.height}, {size.width}, {size.begin_y}, {size.begin_x})"
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
        #     f"border derwin({win_size.height}, {win_size.width}, "
        #     f"{win_size.begin_y}, {win_size.begin_x})"
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
        if self.border:
            if border_win:
                min_h += 2
            else:
                max_h -= 2
        if requested.height is None:
            height = max_h if self.fit == FitType.MAX_FIT else min_h
        else:
            height = requested.height - (2 if (not border_win and self.border) else 0)
        height = min_h if height < min_h else height
        height = max_h if height > max_h else height
        # self.debug(f"calculate_height() {min_h=} {max_h=} {height=}")
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
            width = requested.width - (2 if (not border_win and self.border) else 0)
        width = min_w if width < min_w else width
        width = max_w if width > max_w else width
        # self.debug(
        #     f"calculate_width() req={requested.width} {min_w=} {max_w=} {self.fit=} {width=}"
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
    def handle_keyboard_input(self, key: Keys) -> bool:
        """Handle character input - return if event handled"""
        if key in self.bindings:
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
        self._parent_window = window

    ###################################################################################
    def handle_mouse_event(self, x: int, y: int, bstate: int) -> None:
        """Hande mouse input"""
        # mouse event, represented as a 5-tuple (id, x, y, z, bstate)
        if not self.mouse_bindings:
            return None
        for binding, callback in self.mouse_bindings.items():
            if binding & bstate:
                return callback(x, y, bstate)
        return None


# EOF
