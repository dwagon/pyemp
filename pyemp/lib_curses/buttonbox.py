"""Container for a number of buttons"""

from enum import Enum, auto
from typing import Any

from .button import Button
from .container import Container
from .widget import Widget, FitType


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
        self.focusable = kwargs.get("focusable", False)
        # Where the next button starts
        self.tmp_button_x = 0
        self.tmp_button_y = 0
        self.fit = FitType.MIN_FIT
        self.bindings = {}
        self.bindings.update(kwargs.get("bindings", {}))

    ###################################################################################
    def layout(self):
        """Layout buttons"""
        x_need = self.get_buttons_width()
        y_need = self.get_buttons_height()
        if self.width is None:
            self.width = x_need
        if self.height is None:
            self.height = y_need
        super().layout()

    ###################################################################################
    def get_buttons_width(self) -> int:
        """Return the required_width of all the buttons"""
        width = 0
        for button in self.children_widgets():
            if self.direction == ButtonDirection.HORIZONTAL:
                width += button.required_width + (2 if button.border else 0)
            else:
                width = max(width, button.required_width + (2 if button.border else 0))
        return width

    ###################################################################################
    def get_buttons_height(self) -> int:
        """Return the required_height of all the buttons"""
        height = 0
        for button in self.children_widgets():
            if self.direction == ButtonDirection.VERTICAL:
                height += button.required_height + (2 if button.border else 0)
            else:
                height = max(
                    height, button.required_height + (2 if button.border else 0)
                )
        return height

    ###################################################################################
    @property
    def required_height(self) -> int:
        """Height of the button box"""
        return self.get_buttons_height()

    ###################################################################################
    @property
    def required_width(self) -> int:
        """Width of the button box"""
        return self.get_buttons_width()

    ###################################################################################
    def add(self, widget: Button, name: str = "") -> Widget:
        """Add a button to the box"""
        assert isinstance(
            widget, Button
        ), f"Widgets added to a ButtonBox must be Buttons not {type(widget)}"
        widget.begin_x = self.tmp_button_x
        widget.begin_y = self.tmp_button_y

        super().add(widget, name)
        if self.direction == ButtonDirection.HORIZONTAL:
            self.tmp_button_x += widget.required_width + (2 if widget.border else 0)
        else:
            self.tmp_button_y += widget.required_height + (2 if widget.border else 0)
        return self


# EOF
