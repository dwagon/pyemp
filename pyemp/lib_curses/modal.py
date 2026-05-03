"""Modal Curses Popup"""

import curses
from .keys import Keys
from .widget import Widget


#######################################################################################
#######################################################################################
#######################################################################################
class Modal(Widget):
    """Modal Popup"""

    def __init__(
        self, parent, nlines: int, ncols: int, begin_y: int = 0, begin_x: int = 0
    ):
        super().__init__(parent, begin_y, begin_x)
        self.window = curses.newwin(nlines, ncols, begin_y, begin_x)
        self.window.border()
        self.widgets = []

    def derwin(self, *args, **kwargs):
        """Pass a derwin() call to the parent window"""
        return self.window.derwin(*args, **kwargs)

    def add_widget(self, widget):
        """Add a widget"""
        self.widgets.append(widget)

    def draw(self):
        """Draw the window"""
        self.window.clear()
        self.window.border()
        for widget in self.widgets:
            widget.draw()
        self.window.refresh()

    def mainloop(self):
        """Event loop for modal box"""
        while True:
            self.draw()
            ch = self.window.getch()
            for widget in self.widgets:
                if widget.handle_input(ch):
                    break
                if widget.has_finished():
                    return


# EOF
