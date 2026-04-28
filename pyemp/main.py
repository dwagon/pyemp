"""Main"""

import curses

from pyemp.game import Game

CONFIG = {"server": "localhost", "port": 6665, "country": "1", "password": "1"}


#######################################################################################
def main(stdscr: curses.window):
    """Main"""
    game = Game(CONFIG, stdscr)
    game.initialise_data()
    game.main_loop()


#######################################################################################
if __name__ == "__main__":
    curses.wrapper(main)
