"""Game Object - singleton"""

import curses
import time
from pyemp.comms import setup_socket
from pyemp.misc import login
from pyemp.map_data import MapData
from pyemp.dump import cmd_dump
from pyemp.bmap import cmd_bmap


#######################################################################################
class Game:
    """Game Object"""

    def __init__(self, config: dict[str, int | str], stdscr: curses.window):
        self.stdscr = stdscr
        self.stdscr.clear()
        self.config = config
        self.map = MapData()
        self.x = self.y = 0
        self.init_windows()
        self.sock = setup_socket(config["server"], config["port"])
        next(self.sock)

    def init_windows(self):
        """Initialise windowing"""
        half_way = curses.COLS // 2
        self.map_win = curses.newwin(curses.LINES - 5, half_way)

        self.data_win = curses.newwin(curses.LINES - 5, half_way - 1, 0, half_way + 1)
        self.log_win = curses.newwin(5, curses.COLS, curses.LINES - 5, 0)

    def draw_map(self):
        """Draw the map"""
        self.map_win.clear()
        self.map_win.border()
        map_str = self.map.draw()
        for pos, line in enumerate(map_str.splitlines(), 1):
            self.map_win.addstr(pos, 1, line)

    def refresh_screen(self):
        """Refresh screen"""
        self.log_win.clear()
        self.log_win.border()
        self.log_win.addstr(1, 1, time.ctime())

        self.draw_map()
        self.sector_details()
        self.map_win.refresh()
        self.data_win.refresh()
        self.log_win.refresh()

    def sector_details(self):
        """Fill details about the sector"""
        self.data_win.clear()
        self.data_win.border()
        self.data_win.addstr(1, 1, f"Hex {self.x}, {self.y}")
        if (self.x, self.y) not in self.map:
            return
        m = self.map[(self.x, self.y)]
        self.data_win.addstr(2, 1, m.des)
        self.data_win.addstr(3, 1, f"Civs: {m.civ}, UW: {m.uw}, Mil: {m.mil}")

    def login(self):
        """Login and get an initial dump"""
        login(self.sock, self.config["country"], self.config["password"])
        self.map.update(cmd_dump(self.sock))
        self.map.update(cmd_bmap(self.sock))

    def main_loop(self) -> None:
        """Main event loop"""
        self.refresh_screen()
        while True:
            ch = self.stdscr.getkey()
            match ch:
                case "q":
                    break
                case "g":
                    self.x -= 2
                case "j":
                    self.x += 2
                case "y":
                    self.x -= 1
                    self.y -= 1
                case "u":
                    self.x += 1
                    self.y -= 1
                case "b":
                    self.x -= 1
                    self.y += 1
                case "n":
                    self.x += 1
                    self.y += 1
                case _:
                    pass

            self.refresh_screen()


# EOF
