"""Viewer of multi-line text"""

from typing import Any

from .widget import Widget


#######################################################################################
#######################################################################################
#######################################################################################
class TextViewer(Widget):
    """Text Viewer Widget"""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.text: list[str] = []

    def set_text(self, text: list[str]):
        """Set the text to display"""
        self.text = text

    def draw(self) -> None:
        """Draw the text"""
        for y, line in enumerate(self.text, self.begin_y):
            self.parent.addstr(y, self.begin_x, line)


# EOF
