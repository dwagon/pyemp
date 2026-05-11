"""Button Bar"""

from pyemp.lib_curses import ButtonBox, Button
from pyemp.desig_window import Desig_Window


#######################################################################################
#######################################################################################
#######################################################################################
class ButtonBar(ButtonBox):
    """Window for displaying buttons"""

    def __init__(self, game, **kwargs):
        kwargs["border"] = False
        super().__init__(**kwargs)
        self.game = game
        desig_button = Button(label="Desig", callback=self.desig_callback)
        self.add_button(desig_button)
        thresh_button = Button(label="Thresh", callback=self.thresh_callback)
        self.add_button(thresh_button)

    ###################################################################################
    def desig_callback(self):
        """Someone clicked the Desig button"""
        self.game.log("Desig Callback")
        # dw = Desig_Window(self.x, self.y, self.stdscr, 40, 80, 4, 4)
        # dw.mainloop()
        # if new_desig := dw.get():
        #     cmd_desig(self.sock, self.x, self.y, new_desig)
        #     self.map = update_map(self.sock)

    ###################################################################################
    def thresh_callback(self):
        """The thresh button"""
        self.game.log("Thresh Callback")
