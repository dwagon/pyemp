"""Various mouse events"""

import curses
from enum import IntEnum


#######################################################################################
class MouseEvent(IntEnum):
    """Mouse Events"""

    BUTTON1_CLICKED = curses.BUTTON1_CLICKED
    BUTTON1_PRESSED = curses.BUTTON1_PRESSED
    BUTTON1_RELEASED = curses.BUTTON1_RELEASED
    BUTTON1_DOUBLE_CLICKED = curses.BUTTON1_DOUBLE_CLICKED


# EOF
