"""Popup Dialog"""

from .widget import FitType
from .window import Window
from .textviewer import TextViewer
from .buttonbox import ButtonBox
from .button import Button


#######################################################################################
#######################################################################################
#######################################################################################
class Dialog(Window):
    """Popup Dialog class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = kwargs.get("message", "")
        self.title = kwargs.get("title", "")
        self.button_labels = kwargs.get("buttons", [])
        self.fit = FitType.MIN_FIT
        self.textviewer = None
        self.buttonbox = None
        self.centered = True
        self.border = True

    ###################################################################################
    def layout(self):
        """Layout the dialog"""
        if self._laid_out:
            return
        self.textviewer = self.add(
            TextViewer(text=[self.message], border=False), f"dialog_{self.name}_text"
        )
        self.buttonbox = self.add(
            ButtonBox(begin_y=2, border=False), f"dialog_{self.name}_buttons"
        )
        for button in self.button_labels:
            self.buttonbox.add(Button(label=button))
        self.width = self.required_width
        self.height = self.required_height
        self.root_ui.focus_on_widget(self)
        super().layout()

    ###################################################################################
    @property
    def required_width(self) -> int:
        return max(self.textviewer.required_width, self.buttonbox.required_width)

    ###################################################################################
    @property
    def required_height(self) -> int:
        return self.textviewer.required_height + self.buttonbox.required_height

    ###################################################################################
    def draw(self):
        self._window.erase()
        super().draw()

    ###################################################################################
    def get(self) -> str:
        """Return the label of the button selected"""
        return "TODO"


# EOF
