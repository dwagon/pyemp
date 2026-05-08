"""Game Object - singleton"""

import curses

from pyemp.commands import cmd_desig
from pyemp.comms import setup_socket
from pyemp.data_window import DataWindow
from pyemp.desig_window import Desig_Window
from pyemp.lib_curses import Button, Container, Keys
from pyemp.log_window import LogWindow
from pyemp.map_data import MapData
from pyemp.map_window import MapWindow
from pyemp.misc import initial_map_data, update_map


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
            root=self.stdscr, parent=self.stdscr, nlines=lines, ncols=cols
        )

        self.map_win = MapWindow(
            parent=self.base_container,
            nlines=lines - log_height - button_height,
            ncols=half_way,
            border=True,
            world_x=self.config["WORLD_X"],
            world_y=self.config["WORLD_Y"],
            map=self.map,
        )
        self.data_win = DataWindow(
            parent=self.base_container,
            begin_y=0,
            begin_x=half_way + 1,
            nlines=lines - log_height - button_height,
            ncols=half_way - 1,
            border=True,
        )
        self.log_win = LogWindow(
            parent=self.base_container,
            begin_y=lines - log_height,
            begin_x=0,
            nlines=log_height,
            ncols=cols,
            border=True,
        )
        self.base_container.add_widget(self.map_win)
        self.base_container.add_widget(self.data_win)
        self.base_container.add_widget(self.log_win)

        # self.button_win = Window(
        #    button_height, cols, lines - log_height - button_height, 0
        # )
        # ButtonBar = namedtuple("ButtonBar", ["height", "width", "top_y", "top_x"])
        # self.button_bar = ButtonBar(
        #    button_height, cols, lines - log_height - button_height, 0
        # )
        # self.add_buttons(self.stdscr)

    ###################################################################################
    def log(self, msg: str) -> None:
        """Log a message to the log buffer"""
        self.log_buffer.append(msg)

    ###################################################################################
    def refresh_screen(self):
        """Refresh screen"""
        self.data_win.update(x=self.x, y=self.y, mapdata=self.map)
        self.map_win.update(x=self.x, y=self.y)
        self.log_win.update(self.log_buffer)
        self.base_container.draw()

    ###################################################################################
    def add_buttons(self, win: curses.window):
        """Add the buttons"""
        x_offset = self.button_bar[3]
        y_offset = self.button_bar[2]
        b = Button("Desig", y_offset, x_offset, win, self.desig_callback)
        self.buttons.append(b)
        x_offset += b.width
        b = Button("Thresh", y_offset, x_offset, win, self.thresh_callback)
        self.buttons.append(b)
        x_offset += b.width

    ###################################################################################
    def desig_callback(self):
        """Someone clicked the Desig button"""
        dw = Desig_Window(self.x, self.y, self.stdscr, 40, 80, 4, 4)
        dw.mainloop()
        if new_desig := dw.get():
            cmd_desig(self.sock, self.x, self.y, new_desig)
            self.map = update_map(self.sock)

    ###################################################################################
    def thresh_callback(self):
        """The thresh button"""
        self.log("Thresh Callback")

    ###################################################################################
    def draw_button_window(self):
        """Draw the button window"""
        for line in range(
            self.button_bar.top_y, self.button_bar.top_y + self.button_bar.height
        ):
            self.stdscr.move(line, 0)
            self.stdscr.clrtoeol()
        for button in self.buttons:
            button.draw()

    ###################################################################################
    def main_loop(self) -> None:
        """Main event loop"""
        self.refresh_screen()
        while True:
            # Sadly need getch rather than getkey to handle mouse
            ch = self.stdscr.getch()
            match ch:
                case Keys.KEY_Q:
                    break
                case Keys.KEY_G:
                    self.x -= 2
                case Keys.KEY_J:
                    self.x += 2
                case Keys.KEY_Y:
                    self.x -= 1
                    self.y -= 1
                case Keys.KEY_U:
                    self.x += 1
                    self.y -= 1
                case Keys.KEY_B:
                    self.x -= 1
                    self.y += 1
                case Keys.KEY_N:
                    self.x += 1
                    self.y += 1
                case curses.KEY_MOUSE:
                    self.button_press()
                case _:
                    pass

            self.refresh_screen()

    ###################################################################################
    def button_press(self) -> None:
        """Handle button presses"""
        mouse = curses.getmouse()
        if mouse[4] & curses.BUTTON1_CLICKED:
            for button in self.buttons:
                if button.is_clicked(mouse[2], mouse[1]):
                    self.log(f"Clicked on {button.label}")
                    button.do_callback()
                    self.refresh_screen()


# EOF
