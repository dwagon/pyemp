"""Log Window"""

from pyemp.lib_curses import TextViewer


#######################################################################################
#######################################################################################
#######################################################################################
class LogWindow(TextViewer):
    """Window for displaying logs"""

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.border = True
        self.game = game
        self.focusable = False
        self.name = "Log Display"

    def update(self, log_buffer: list[str]):
        """Update the logs"""
        if not self._window:
            return
        max_y, _ = self._window.getmaxyx()
        vert_size = max_y - 2  # How many lines we can display (2 for border)

        self.set_text(log_buffer[-vert_size:])


# EOF
