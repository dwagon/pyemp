"""Various mouse events"""

import curses
from enum import IntEnum


#######################################################################################
class MouseEvent(IntEnum):
    """Mouse Events"""

    BUTTON1_CLICKED = curses.BUTTON1_CLICKED


# EOF
