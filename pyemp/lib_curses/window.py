"""Window"""

import curses

from .widget import FitType
from .container import Container


#######################################################################################
#######################################################################################
#######################################################################################
class Window(Container):
    """Curses Window"""

    def __init__(self, **kwargs):
        self.centered = kwargs.get("centered", False)
        self.fit = kwargs.get("fit", FitType.MAX_FIT)
        super().__init__(**kwargs)

    ###################################################################################
    def layout(self):
        """Layout the window"""
        if self.centered:
            width = self.width if self.width else 1
            height = self.height if self.height else 1
            self.begin_x = (curses.COLS - width) // 2  # pylint: disable=no-member
            self.begin_y = (curses.LINES - height) // 2  # pylint: disable=no-member
        super().layout()


# EOF
