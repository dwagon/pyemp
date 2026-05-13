"""Container for a number of buttons"""

from typing import Any
from enum import Enum, auto

from .container import Container
from .button import Button


#######################################################################################
class ButtonAlignment(Enum):
    """Which direction to make buttons go"""

    HORIZONTAL = auto()
    VERTICAL = auto()


#######################################################################################
#######################################################################################
#######################################################################################
class ButtonBox(Container):
    """ButtonBox Widget"""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.alignment: ButtonAlignment = kwargs.get(
            "alignment", ButtonAlignment.HORIZONTAL
        )
        self.tmp_x = 1 if self.border else 0
        self.tmp_y = 1 if self.border else 0

    ###################################################################################
    def add_button(self, button: Button):
        """Add a button to the box"""
        button.begin_x = self.tmp_x
        button.begin_y = self.tmp_y

        self.add(f"button_{button.label}", button)
        if self.alignment == ButtonAlignment.HORIZONTAL:
            self.tmp_x += button.width
        else:
            self.tmp_y += button.height


# EOF
