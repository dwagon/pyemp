"""Data window for map display"""

import curses

from pyemp.lib_curses import Container, TextViewer, Keys


#######################################################################################
#######################################################################################
#######################################################################################
class MapWindow(Container):
    """Window for displaying map data"""

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.border = True
        self.world_x = kwargs.get("world_x")
        self.world_y = kwargs.get("world_y")
        self.map = kwargs.get("map")
        self.add("display", TextViewer(begin_x=1, begin_y=1))
        self.x = 0
        self.y = 0
        self.bindings = {
            Keys.KEY_G: self.move_left,
            Keys.KEY_J: self.move_right,
            Keys.KEY_Y: self.move_up_left,
            Keys.KEY_U: self.move_up_right,
            Keys.KEY_B: self.move_down_left,
            Keys.KEY_N: self.move_down_right,
        }

    ###################################################################################
    def get_coords(self) -> tuple[int, int]:
        """Set the coords we are looking at"""
        return self.x, self.y

    ###################################################################################
    def move_left(self) -> None:
        """move cursor left in map"""
        self.x -= 2

    ###################################################################################
    def move_right(self) -> None:
        """move cursor right in map"""
        self.x += 2

    ###################################################################################
    def move_up_left(self) -> None:
        """move cursor up and left in map"""
        self.x -= 1
        self.y -= 1

    ###################################################################################
    def move_up_right(self) -> None:
        """move cursor up and right in map"""
        self.x += 1
        self.y -= 1

    ###################################################################################
    def move_down_left(self) -> None:
        """move cursor down and left in map"""
        self.x -= 1
        self.y += 1

    ###################################################################################
    def move_down_right(self) -> None:
        """move cursor down and right in map"""
        self.x += 1
        self.y += 1

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
