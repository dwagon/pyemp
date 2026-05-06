"""Keys - has to be a class rather than a variable for the match/case to work"""

import curses.ascii

#######################################################################################
#######################################################################################
#######################################################################################


class Keys:
    """Keys definitions"""

    KEY_A = ord("a")
    KEY_B = ord("b")
    KEY_C = ord("c")
    KEY_D = ord("d")
    KEY_DOWN = curses.KEY_DOWN
    KEY_ENTER = curses.KEY_ENTER
    KEY_ESC = curses.ascii.ESC
    KEY_G = ord("g")
    KEY_J = ord("j")
    KEY_K = ord("k")
    KEY_N = ord("n")
    KEY_Q = ord("q")
    KEY_RETURN = ord("\n")
    KEY_S = ord("s")
    KEY_U = ord("u")
    KEY_UP = curses.KEY_UP
    KEY_W = ord("w")
    KEY_Y = ord("y")
    KEY_Z = ord("z")
