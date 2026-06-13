"""Designate Sector code"""

from typing import Optional

from .lib_curses import Window, Keys, Label, Listbox, FitType, Button
from .sector import DESIG_KEY_MAP


#######################################################################################
#######################################################################################
#######################################################################################
class Desig_Window(Window):
    """Popup Designate Sector {x,y} Window"""

    def __init__(self, x: int, y: int):
        super().__init__(
            centered=True,
            border=True,
            fit=FitType.MIN_FIT,
            bindings={Keys.KEY_ENTER: self.close},
        )
        self.new_desig: str = ""
        self.x = x
        self.y = y
        self.listbox = None
        self.modal_focus = True

    ###################################################################################
    def layout(self):
        """Add widgets"""
        dopts = designatable_options()
        self.add(Label(text=f"Designate Sector ({self.x}, {self.y})"))
        self.listbox = Listbox(begin_y=2)
        for desig, descr in dopts.items():
            self.listbox.add_entry(desig, f"{desig} {descr}")
        self.add(self.listbox)
        self.width = self.required_width
        self.height = self.required_height
        self.add(Button(label="Cancel", begin_y=len(dopts) + 3, callback=None))
        self.add(
            Button(label="Designate", begin_y=len(dopts) + 3, begin_x=15, callback=None)
        )
        self.root_ui.focus_on_widget(self.listbox)
        super().layout()

    ###################################################################################
    @property
    def required_height(self) -> int:
        """Height of window"""
        height = len(designatable_options()) + 4 + 4  # 4 for label
        return height

    ###################################################################################
    @property
    def required_width(self) -> int:
        """Width of window"""
        return max(30, max(len(_) for _ in designatable_options().values()))

    ###################################################################################
    def get(self) -> Optional[str]:
        """Return result"""
        return self.new_desig

    ###################################################################################
    def close(self) -> None:
        """User has made the selection"""
        self.root_ui.delete(self)


###################################################################################
def designatable_options() -> dict[str, str]:
    """Return map of choices that the user can specify"""
    new_map = {}
    for desig, descr in DESIG_KEY_MAP.items():
        if desig in ("?", ".", "^", "s", "-", "~", "\\"):  # Can't be designated as
            continue
        new_map[desig] = descr
    return new_map


# EOF
