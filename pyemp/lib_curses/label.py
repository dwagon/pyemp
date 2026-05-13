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
        self.text = kwargs.get("text", "")

    def draw(self):
        """Draw the label"""
        self.parent.addstr(self.begin_y, self.begin_x, self.text)

    def set_text(self, text: str):
        """Set the text"""
        self.text = text


# EOF
