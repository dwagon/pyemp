"""Simple String Label Widget"""

from typing import Any

from .widget import Widget, FitType


#######################################################################################
#######################################################################################
#######################################################################################
class Label(Widget):
    """Label Widget"""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.text = kwargs.get("text", "")
        self.focusable = False
        self.fit = kwargs.get("fit", FitType.MIN_FIT)

    ###################################################################################
    def draw(self):
        """Draw the label"""
        super().draw()
        self._window.addstr(0, 0, self.text)

    ###################################################################################
    def set_text(self, text: str):
        """Set the text"""
        self.text = text

    ###################################################################################
    def assign_name(self) -> str:
        """Assign a name if one isn't given"""
        return f"Label {self.text[:8]}"

    ###################################################################################
    @property
    def required_height(self) -> int:
        """required_height of widget"""
        return 1

    ###################################################################################
    @property
    def required_width(self) -> int:
        """required_width of widget"""
        return len(self.text) + 1


# EOF
