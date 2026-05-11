"""Log Window"""

from pyemp.lib_curses import Container, TextViewer


#######################################################################################
#######################################################################################
#######################################################################################
class LogWindow(Container):
    """Window for displaying logs"""

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.log_display = TextViewer(**kwargs)
        self.add_widget(self.log_display)

    def update(self, log_buffer: list[str]):
        """Update the logs"""
        max_y, _ = self.getmaxyx()
        vert_size = max_y - 2  # How many lines we can display (2 for border)

        self.log_display.set_text(log_buffer[-vert_size:])


# EOF
