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
        self.focusable = False

    ###################################################################################
    def draw(self):
        """Draw the label"""
        super().draw()
        self._window.addstr(self.begin_y, self.begin_x, self.text)

    ###################################################################################
    def set_text(self, text: str):
        """Set the text"""
        self.text = text

    ###################################################################################
    def assig_name(self) -> str:
        """Assign a name if one isn't given"""
        return f"Label {self.text[:8]}"

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
