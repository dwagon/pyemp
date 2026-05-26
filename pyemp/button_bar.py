"""Button Bar"""

from pyemp.lib_curses import ButtonBox, Button


#######################################################################################
#######################################################################################
#######################################################################################
class ButtonBar(ButtonBox):
    """Window for displaying buttons"""

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.border = False
        self.game = game

    ###################################################################################
    def layout(self):
        """Layout the buttons"""
        self.add(Button(label="Designate", callback=self.desig_callback))
        self.add(Button(label="Threshold", callback=self.thresh_callback))
        super().layout()

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
