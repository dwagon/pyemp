"""Popup Dialog"""

from typing import Optional

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
        self.buttons = kwargs.get("buttons", [])
        self.fit = FitType.MIN_FIT
        self.textviewer = None
        self.focusable = False
        self.buttonbox = None
        self.centered = True
        self.border = True

    ###################################################################################
    def add_button(self, button: Button) -> None:
        """Add buttons to an existing dialog"""
        self.buttons.append(button)

    ###################################################################################
    def close_dialog(self):
        """Close the dialog box"""
        self.root_ui.delete(self)

    ###################################################################################
    def layout(self):
        """Layout the dialog"""
        if self._laid_out:
            return
        if isinstance(self.message, str):
            msg = [self.message]
        else:
            msg = self.message
        self.textviewer = self.add(
            TextViewer(text=msg, border=False), f"dialog_{self.name}_text"
        )
        self.buttonbox = self.add(
            ButtonBox(begin_y=1 + len(msg), border=False, modal_focus=True),
            f"dialog_{self.name}_buttons",
        )
        for button in self.buttons:
            self.buttonbox.add(button)
        self.width = self.required_width
        self.height = self.required_height
        super().layout()
        self.root_ui.focus_on_widget(self.buttonbox)

    ###################################################################################
    @property
    def required_width(self) -> int:
        """Required width of dialog"""
        return max(self.textviewer.required_width, self.buttonbox.required_width) + 2

    ###################################################################################
    @property
    def required_height(self) -> int:
        """Required height of dialog"""
        return self.textviewer.required_height + self.buttonbox.required_height + 2

    ###################################################################################
    def get(self) -> Optional[str]:
        """Return the label of the button selected"""
        return self.buttonbox.get()


#######################################################################################
#######################################################################################
#######################################################################################
class ErrorDialog(Dialog):
    """Error Dialog"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.buttons:
            button = Button(label="OK", callback=self.close_dialog)
            self.add_button(button)
        if not kwargs.get("alert_icon", None):
            self.message = [
                "    _",
                "   / \\",
                f"  / ! \\   {self.message}",
                " /_____\\",
            ]

        # EOF
