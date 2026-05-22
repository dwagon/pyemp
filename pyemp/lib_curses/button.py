"""Curses based button"""

import curses
from typing import Optional, Callable, Any
from .widget import Widget, FitType
from .mouse_events import MouseEvent


#######################################################################################
#######################################################################################
#######################################################################################
class Button(Widget):
    """Button Widget"""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.label = kwargs["label"]
        self.value = kwargs.get("value", "")
        self.callback: Optional[Callable[[], None]] = kwargs.get("callback", None)
        self.border: bool = kwargs.get("border", True)
        self.mouse_bindings = {MouseEvent.BUTTON1_CLICKED: self.clicked}
        self.fit = FitType.MIN_FIT
        self.selected = kwargs.get("selected", False)

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
    def clicked(self, x: int, y: int):
        """Button was selected"""
        y1, x1 = self._window.getbegyx()
        y2, x2 = self._window.getmaxyx()
        if x1 < x < x2 and y1 < y < y2:
            if self.callback:
                self.callback()

    ###################################################################################
    def is_clicked(self, mouse_y: int, mouse_x: int) -> bool:
        """Did the user click on the button"""
        # min_y, min_x = self.window.getbegyx()
        # max_y, max_x = self.window.getmaxyx()
        # if min_y < mouse_y < max_y + min_y and min_x < mouse_x < max_x + min_x:
        #     return True
        # return False

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
