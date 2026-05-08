"""Data window for map display"""

import curses

from pyemp.lib_curses import Container, TextViewer


#######################################################################################
#######################################################################################
#######################################################################################
class MapWindow(Container):
    """Window for displaying map data"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.map_display = TextViewer(begin_x=1, begin_y=1)
        self.border = True
        self.world_x = kwargs.get("world_x")
        self.world_y = kwargs.get("world_y")
        self.map = kwargs.get("map")
        self.add_widget(self.map_display)
        self.x = 0
        self.y = 0

    ###################################################################################
    def update(self, x: int, y: int):
        """Set the coords we are looking at"""
        self.x = x
        self.y = y

    ###################################################################################
    def draw(self):
        """Draw the map"""
        for a in range(-self.world_x // 2, self.world_x // 2):
            for b in range(-self.world_y // 2, self.world_y // 2):
                if self.x == a and self.y == b:
                    attr = curses.A_REVERSE
                else:
                    attr = curses.A_NORMAL
                self.parent.addstr(
                    b + self.world_y // 2,
                    a + self.world_x // 2,
                    self.map[a, b].des,
                    attr,
                )
