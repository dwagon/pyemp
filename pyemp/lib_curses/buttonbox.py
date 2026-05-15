"""Container for a number of buttons"""

from typing import Any
from enum import Enum, auto

from .container import Container
from .button import Button


#######################################################################################
class ButtonDirection(Enum):
    """Which direction to make buttons go"""

    HORIZONTAL = auto()
    VERTICAL = auto()


#######################################################################################
class ButtonAlignment(Enum):
    """Alignment of buttons in box"""

    LEFT = auto()
    MIDDLE = auto()
    RIGHT = auto()


#######################################################################################
#######################################################################################
#######################################################################################
class ButtonBox(Container):
    """ButtonBox Widget"""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.direction: ButtonDirection = kwargs.get(
            "direction", ButtonDirection.HORIZONTAL
        )
        self.alignment: ButtonAlignment = kwargs.get("alignment", ButtonAlignment.LEFT)
        # Where the next button starts
        self.tmp_button_x = 1 if self.border else 0
        self.tmp_button_y = 1 if self.border else 0

    ###################################################################################
    def layout(self):
        """Layout buttons"""
        x_need = self.get_buttons_width()
        y_need = self.get_buttons_height()
        self.debug(f"{self} {x_need=} {y_need=}")
        if self.ncols < 0:
            self.ncols = x_need + 1
        if self.nlines < 0:
            self.nlines = y_need + 1
        self.debug(f"{self} {self.ncols=} {self.nlines=}")
        super().layout()

    ###################################################################################
    def get_buttons_width(self) -> int:
        """Return the width of all the buttons"""
        width = 0
        for button in self._widgets.values():
            if self.direction == ButtonDirection.HORIZONTAL:
                width += button.width
            else:
                width = max(width, button.width)
        return width

    ###################################################################################
    def get_buttons_height(self) -> int:
        """Return the height of all the buttons"""
        height = 0
        for button in self._widgets.values():
            if self.direction == ButtonDirection.VERTICAL:
                height += button.height
            else:
                height = max(height, button.height)
        return height

    ###################################################################################
    @property
    def height(self) -> int:
        """Height of the button box"""
        return self.get_buttons_height()

    ###################################################################################
    @property
    def width(self) -> int:
        """Width of the button box"""
        return self.get_buttons_width()

    ###################################################################################
    def add(self, name: str, widget: Button):
        """Add a button to the box"""
        widget.begin_x = self.tmp_button_x
        widget.begin_y = self.tmp_button_y

        super().add(name, widget)
        if self.direction == ButtonDirection.HORIZONTAL:
            self.tmp_button_x += widget.width
        else:
            self.tmp_button_y += widget.height


# EOF
