"""Game Object - singleton"""

import curses
import sys

from pyemp.button_bar import ButtonBar
from pyemp.comms import setup_socket
from pyemp.data_window import DataWindow
from pyemp.lib_curses import UI, Window, Keys
from pyemp.log_window import LogWindow
from pyemp.map_data import MapData
from pyemp.map_window import MapWindow
from pyemp.misc import initial_map_data


#######################################################################################
#######################################################################################
#######################################################################################
class Game:
    """Game Object"""

    def __init__(self, config: dict[str, int | str], stdscr: curses.window):
        self.ui = UI(stdscr)

        self.config = config
        self.map = MapData()
        self.x = self.y = 0
        self.buttons = []
        self.sock = setup_socket(config["server"], config["port"])
        next(self.sock)
        self.base_window = None
        self.data_win = None
        self.map_win = None
        self.log_win = None
        self.button_bar = None
        self.log_buffer: list[str] = []

        self.initialise_data()
        self.init_windows()

    ###################################################################################
    def initialise_data(self):
        """Initialise game data"""
        self.map = initial_map_data(self.sock, self.config)

    ###################################################################################
    def init_windows(self):
        """Initialise windowing"""
        lines = curses.LINES  # pylint: disable=no-member
        cols = curses.COLS  # pylint: disable=no-member
        half_way = cols // 2
        log_height = 7
        button_height = 3
        self.base_window = self.ui.add(
            Window(
                height=lines,
                width=cols,
                name="Game",
                bindings={Keys.KEY_Q: self.quit},
            ),
        )
        self.map_win = self.base_window.add(
            MapWindow(
                self,
                height=lines - log_height - button_height,
                width=half_way,
                world_x=self.config["WORLD_X"],
                world_y=self.config["WORLD_Y"],
                map=self.map,
            ),
            "map",
        )
        self.data_win = self.base_window.add(
            DataWindow(
                self,
                begin_y=0,
                begin_x=half_way + 1,
                height=lines - log_height - button_height,
                width=half_way - 1,
            ),
            "data",
        )
        self.log_win = self.base_window.add(
            LogWindow(
                self,
                begin_y=lines - log_height,
                begin_x=0,
                height=log_height,
                width=cols,
            ),
            "log",
        )
        self.base_window.add(
            ButtonBar(
                self,
                begin_y=lines - log_height - button_height,
                begin_x=0,
                height=button_height,
                width=cols,
            ),
            "buttons",
        )
        self.ui.focus_on(self.map_win)

    ###################################################################################
    def quit(self) -> None:
        """quit app"""
        sys.exit(0)

    ###################################################################################
    def log(self, msg: str) -> None:
        """Log a message to the log buffer"""
        self.log_buffer.append(msg)

    ###################################################################################
    def refresh_screen(self):
        """Refresh screen"""
        self.x, self.y = self.map_win.get_coords()
        self.data_win.update(x=self.x, y=self.y, mapdata=self.map)
        self.log_win.update(self.log_buffer)

    ###################################################################################
    def main_loop(self) -> None:
        """Main event loop"""
        self.refresh_screen()
        self.ui.mainloop()


# EOF
