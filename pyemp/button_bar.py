"""Button Bar"""

from pyemp.lib_curses import ButtonBox, Button
from .desig_window import Desig_Window


#######################################################################################
#######################################################################################
#######################################################################################
class ButtonBar(ButtonBox):
    """Window for displaying buttons"""

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.border = False
        self.game = game
        self.focusable = False

    ###################################################################################
    def layout(self):
        """Layout the buttons"""
        if self._laid_out:
            return
        self.add(Button(label="Designate", callback=self.desig_callback))
        self.add(Button(label="Threshold", callback=self.thresh_callback))
        super().layout()

    ###################################################################################
    def desig_callback(self):
        """Someone clicked the Desig button"""
        self.game.log("Desig Callback")
        dw = Desig_Window(self.game.x, self.game.y)
        self.game.base_window.add(dw)
        self.debug(f"Added desig {dw} {dw._parent_window=}")

        # dw.mainloop()
        # if new_desig := dw.get():
        #     cmd_desig(self.sock, self.x, self.y, new_desig)
        #     self.map = update_map(self.sock)

    ###################################################################################
    def thresh_callback(self):
        """The thresh button"""
        self.game.log("Thresh Callback")
