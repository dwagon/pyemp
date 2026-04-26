"""Game Object - singleton"""

import curses
import time
import tabulate
from pyemp.comms import setup_socket
from pyemp.commands import cmd_vers, cmd_dump, cmd_bmap
from pyemp.misc import login
from pyemp.map_data import MapData
from pyemp.dump import cmd_dump
from pyemp.bmap import cmd_bmap
from pyemp.vers import cmd_vers
from pyemp.sector import Sector, desig_name


class Keys:
    """Keys - has to be a class rather than a variable for the match/case to work"""

    KEY_B = ord("b")
    KEY_G = ord("g")
    KEY_J = ord("j")
    KEY_N = ord("n")
    KEY_Q = ord("q")
    KEY_U = ord("u")
    KEY_Y = ord("y")


#######################################################################################
#######################################################################################
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
        self.log_buffer = []

    ###################################################################################
    def init_windows(self):
        """Initialise windowing"""
        lines = curses.LINES  # pylint: disable=no-member
        cols = curses.COLS  # pylint: disable=no-member
        half_way = cols // 2
        log_height = 7

        self.map_win = curses.newwin(lines - log_height, half_way)
        self.data_win = curses.newwin(lines - log_height, half_way - 1, 0, half_way + 1)
        self.log_win = curses.newwin(log_height, cols, lines - log_height, 0)

        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        self.stdscr.keypad(1)

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
    def draw_log_win(self):
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
        self.draw_log_win()
        self.draw_map()
        self.draw_data_window()

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
        des_str = get_design_str(m)
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
            "Fert: {m.fert}, Oil: {m.ocontent}, Uranium {m.uran}",
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
    def login(self):
        """Login and get an initial dump"""
        login(self.sock, self.config["country"], self.config["password"])
        self.map.update(cmd_dump(self.sock))
        self.map.update(cmd_bmap(self.sock))
        vers_config = cmd_vers(self.sock)
        for var in ("WORLD_X", "WORLD_Y"):
            self.config[var] = vers_config[var]
        self.fill_map()

    ###################################################################################
    def fill_map(self):
        """Fill the empty spots of the map in"""
        m = MapData()
        for x in range(-self.config["WORLD_X"] // 2, self.config["WORLD_X"] // 2):
            for y in range(-self.config["WORLD_Y"] // 2, self.config["WORLD_Y"] // 2):
                m.add(Sector(x, y, ""))
        self.map.update(m)

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
                    mouse = curses.getmouse()
                    self.log(f"Mouse: {mouse[1]}, {mouse[2]} Button {mouse[4]}")
                case _:
                    pass

            self.refresh_screen()


###################################################################################
def get_design_str(m: Sector) -> str:
    """Return the designation details for the current sector"""
    des_str = ""
    if m.des:
        des_str = f"{desig_name(m.des).title()} ({m.des})"
    if m.sdes and m.sdes != " ":
        des_str += f" Becoming {desig_name(m.sdes).title()} ({m.sdes})"
    return des_str


# EOF
