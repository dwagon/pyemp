"""Simple String Label Widget"""

from typing import Any

from .widget import Widget


#######################################################################################
#######################################################################################
#######################################################################################
class Label(Widget):
    """Label Widget"""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.text = kwargs.get("text", "XXXXXXXX")

    ###################################################################################
    def draw(self):
        """Draw the label"""
        super().draw()
        self.window.addstr(self.text)

    ###################################################################################
    def set_text(self, text: str):
        """Set the text"""
        self.text = text

    ###################################################################################
    @property
    def height(self) -> int:
        """height of widget"""
        return 1

    ###################################################################################
    @property
    def width(self) -> int:
        """width of widget"""
        return len(self.text) + 1


# EOF
