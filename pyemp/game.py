"""Game Object - singleton"""

import curses
import sys
from pyemp.comms import setup_socket
from pyemp.data_window import DataWindow
from pyemp.button_bar import ButtonBar
from pyemp.lib_curses import Container, Keys
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
        self.stdscr = stdscr

        self.config = config
        self.map = MapData()
        self.x = self.y = 0
        self.buttons = []
        self.sock = setup_socket(config["server"], config["port"])
        next(self.sock)

        self.data_win = None
        self.map_win = None
        self.log_win = None
        self.button_bar = None
        self.log_buffer: list[str] = []

        self.initialise_data()
        self.init_windows()

        print("DBG Game", file=open("/tmp/err", "w"))

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

        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        curses.curs_set(0)  # Invisible cursor
        self.stdscr.keypad(True)

        self.base_container = Container(
            root=self.stdscr,
            parent=self.stdscr,
            nlines=lines,
            ncols=cols,
            bindings={Keys.KEY_Q: self.quit},
        )

        self.map_win = MapWindow(
            self,
            parent=self.base_container,
            nlines=lines - log_height - button_height,
            ncols=half_way,
            border=True,
            world_x=self.config["WORLD_X"],
            world_y=self.config["WORLD_Y"],
            map=self.map,
        )
        self.data_win = DataWindow(
            self,
            parent=self.base_container,
            begin_y=0,
            begin_x=half_way + 1,
            nlines=lines - log_height - button_height,
            ncols=half_way - 1,
            border=True,
        )
        self.log_win = LogWindow(
            self,
            parent=self.base_container,
            begin_y=lines - log_height,
            begin_x=0,
            nlines=log_height,
            ncols=cols,
            border=True,
        )
        self.button_bar = ButtonBar(
            self,
            parent=self.base_container,
            begin_y=lines - log_height - button_height,
            begin_x=0,
            nlines=button_height,
            ncols=cols,
        )
        self.base_container.add_widget(self.map_win)
        self.base_container.add_widget(self.data_win)
        self.base_container.add_widget(self.log_win)
        self.base_container.add_widget(self.button_bar)

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
        self.base_container.draw()

    ###################################################################################
    def main_loop(self) -> None:
        """Main event loop"""
        self.refresh_screen()
        self.base_container.mainloop()


# EOF
