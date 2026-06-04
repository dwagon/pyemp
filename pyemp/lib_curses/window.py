"""Window"""

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

    def layout(self):
        """Layout the window"""
        if self.centered:
            if not self.width:
                self.width = self.avail_width()
            if not self.height:
                self.height = self.avail_height()
            self.begin_x = (self.avail_width() - self.width) // 2
            self.begin_y = (self.avail_height() - self.height) // 2
        super().layout()


# EOF
