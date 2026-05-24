"""Viewer of multi-line text"""

from typing import Any

from .widget import Widget, FitType


#######################################################################################
#######################################################################################
#######################################################################################
class TextViewer(Widget):
    """Text Viewer Widget"""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.text: list[str] = []
        self.fit = FitType.MIN_FIT

    ###################################################################################
    def set_text(self, text: list[str]):
        """Set the text to display"""
        self.text = text

    ###################################################################################
    def draw(self) -> None:
        """Draw the text"""
        super().draw()
        for y, line in enumerate(self.text):
            self._window.addstr(y, 0, line)

    ###################################################################################
    @property
    def required_width(self) -> int:
        if not self.text:
            return 1
        return max(len(_) for _ in self.text)

    ###################################################################################
    @property
    def required_height(self) -> int:
        if not self.text:
            return 1
        return len(self.text)


# EOF
