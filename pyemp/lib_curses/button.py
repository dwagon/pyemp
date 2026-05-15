"""Curses based button"""

from typing import Optional, Callable, Any
from .widget import Widget
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

    ###################################################################################
    def draw(self):
        """Draw the button"""
        super().draw()
        self.window.addstr(0, 0, self.label)

    ###################################################################################
    def clicked(self, x: int, y: int):
        """Button was selected"""
        y1, x1 = self.window.getbegyx()
        y2, x2 = self.window.getmaxyx()
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
    def width(self) -> int:
        """Width of the button"""
        return len(self.label) + (2 if self.border else 0)

    ###################################################################################
    @property
    def height(self) -> int:
        """Height of the button"""
        return 1 + (2 if self.border else 0)

    ###################################################################################
    def __repr__(self):
        return f"<Button {self.label}>"


# EOF
