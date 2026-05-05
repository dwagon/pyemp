"""Game Object - singleton"""

import curses
from collections import namedtuple
import tabulate

from pyemp.lib_curses.button import Button
from pyemp.lib_curses.keys import Keys
from pyemp.comms import setup_socket
from pyemp.map_data import MapData
from pyemp.misc import initial_map_data, debug, update_map
from pyemp.sector import Sector, desig_name
from pyemp.desig_window import Desig_Window
from pyemp.commands import cmd_desig


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
        self.init_windows()
        self.sock = setup_socket(config["server"], config["port"])
        next(self.sock)
        self.log_buffer = []
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
        self.stdscr.clear()

        self.map_win = curses.newwin(lines - log_height - button_height, half_way)
        self.data_win = curses.newwin(
            lines - log_height - button_height, half_way - 1, 0, half_way + 1
        )
        self.log_win = curses.newwin(log_height, cols, lines - log_height, 0)

        # self.button_win = curses.newwin(
        #    button_height, cols, lines - log_height - button_height, 0
        # )
        ButtonBar = namedtuple("ButtonBar", ["height", "width", "top_y", "top_x"])
        self.button_bar = ButtonBar(
            button_height, cols, lines - log_height - button_height, 0
        )
        self.add_buttons(self.stdscr)
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        curses.curs_set(0)  # Invisible cursor
        self.stdscr.keypad(True)

    ###################################################################################
    def draw_map(self):
        """Draw the map"""
        self.map_win.clear()
        self.map_win.border()

        for x in range(-self.config["WORLD_X"] // 2, self.config["WORLD_X"] // 2):
            for y in range(-self.config["WORLD_Y"] // 2, self.config["WORLD_Y"] // 2):
                if (x, y) in self.map:
                    if self.x == x and self.y == y:
                        attr = curses.A_REVERSE
                    else:
                        attr = curses.A_NORMAL
                    self.stdscr.addstr(
                        y + self.config["WORLD_Y"] // 2,
                        x + self.config["WORLD_X"] // 2,
                        self.map[x, y].des,
                        attr,
                    )
        self.map_win.refresh()

    ###################################################################################
    def log(self, msg: str) -> None:
        """Log a message to the log buffer"""
        self.log_buffer.append(msg)

    ###################################################################################
    def draw_log_window(self):
        """Draw the log window"""
        max_y, _ = self.log_win.getmaxyx()
        vert_size = max_y - 2  # How many lines we can display (2 for border)
        self.log_win.clear()
        self.log_win.border()

        for y, line in enumerate(self.log_buffer[-vert_size:], 1):
            self.log_win.addstr(y, 1, line)
        self.log_win.refresh()

    ###################################################################################
    def refresh_screen(self):
        """Refresh screen"""
        self.draw_log_window()
        self.draw_data_window()
        self.draw_button_window()
        self.draw_map()

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
        new_desig = dw.get()
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
    def draw_data_window(self):
        """Manage the data window"""
        self.data_win.clear()
        self.data_win.border()
        self.sector_details()
        self.data_win.refresh()

    ###################################################################################
    def sector_details(self):
        """Fill details about the sector"""

        self.data_win.addstr(1, 1, f"Hex {self.x}, {self.y}")
        if (self.x, self.y) not in self.map:
            return
        m = self.map[(self.x, self.y)]
        des_str = get_desig_str(m)
        self.data_win.addstr(2, 1, des_str)
        self.data_win.addstr(
            3,
            1,
            f"Civs: {m.civ}/{m.c_dist}, UW: {m.uw}/{m.u_dist}, Mil: {m.mil}/{m.m_dist}",
        )
        self.data_win.addstr(
            4,
            1,
            f"Resource: Iron: {m.min}, Gold: {m.gold}, "
            f"Fert: {m.fert}, Oil: {m.ocontent}, Uranium {m.uran}",
        )
        table = self.distribution_details_table()
        for y, line in enumerate(table.splitlines(), 6):
            self.data_win.addstr(y, 1, line)

    ###################################################################################
    def distribution_details_table(self) -> str:
        """Return the details about commodity distribution"""
        commodities = [
            ("Shells", "shell", "s_dist", "s_del", "s_cut"),
            ("Guns", "gun", "g_dist", "g_del", "g_cut"),
            ("Petrol", "pet", "p_dist", "p_del", "p_cut"),
            ("Iron", "iron", "i_dist", "i_del", "i_cut"),
            ("Gold Dust", "dust", "d_dist", "d_del", "d_cut"),
            ("Gold Bars", "bar", "b_dist", "b_del", "b_cut"),
            ("Oil", "oil", "s_dist", "o_del", "o_cut"),
            ("Light CM", "lcm", "l_dist", "l_del", "l_cut"),
            ("Heavy CM", "hcm", "h_dist", "h_del", "h_cut"),
            ("Rads", "rad", "r_dist", "r_del", "r_cut"),
        ]
        headers = ["Commodity", "Amount", "Threshold", "Deliver", "Cutoff"]
        m = self.map[(self.x, self.y)]

        table = []
        for name, amnt, thresh, deliv, cutoff in commodities:
            line = [name, m[amnt]]
            if m[thresh]:
                line.append(m[thresh])
            else:
                line.append("")
            if m[deliv]:
                line.append(m[deliv])
            else:
                line.append("")
            if m[cutoff]:
                line.append(m[cutoff])
            else:
                line.append("")
            table.append(line)
        return tabulate.tabulate(table, headers=headers)

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


###################################################################################
def get_desig_str(m: Sector) -> str:
    """Return the designation details for the current sector"""
    des_str = ""
    if m.des:
        des_str = f"{desig_name(m.des).title()} ({m.des})"
    if m.sdes and m.sdes != " ":
        des_str += f" Becoming {desig_name(m.sdes).title()} ({m.sdes})"
    return des_str


# EOF
