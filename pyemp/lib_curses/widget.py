"""Parent class for widgets"""

import curses
from enum import StrEnum, auto
from typing import Callable, Any, Self, Optional

import treelib

from .keys import Keys
from .widget_layout import WidgetLayout, FitType
from .mouse_events import MouseEvent


#######################################################################################
class BindingName(StrEnum):
    """Event Binding names"""

    GAIN_FOCUS = auto()
    LOSE_FOCUS = auto()


#######################################################################################
#######################################################################################
#######################################################################################
class Widget(WidgetLayout):
    """Generic Widget Class"""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

        self.name = kwargs.get("name", "")
        self.focusable = kwargs.get("focusable", True)
        self.focus = False
        self.modal_focus = kwargs.get("modal_focus", False)
        self.root_ui = None
        self.node_id = ""
        self.bindings: dict[Keys, Callable[[], None]] = kwargs.get("bindings", {})
        self.mouse_bindings: dict[MouseEvent, Callable[[int, int, int], None]] = {}
        self.misc_bindings: dict[BindingName, Optional[Callable[[], None]]] = {
            BindingName.GAIN_FOCUS: kwargs.get("gainfocus"),
            BindingName.LOSE_FOCUS: kwargs.get("loosefocus"),
        }
        self.update_callback = kwargs.get("update_callback", None)

    ###################################################################################
    @property
    def widget_tree(self) -> treelib.Tree:
        """Shortcut to the widget tree"""
        return self.root_ui.widget_tree

    ###################################################################################
    def enclose(self, y: int, x: int) -> bool:
        """Is the coord in our window?"""
        if not self._window:
            self.debug(f"{self=}\n{self.root_ui.widget_tree.show(stdout=False)}")
        return self._window.enclose(y, x)

    ###################################################################################
    def gainFocus(self):
        """This widget has received focus"""
        if self.modal_focus:
            self.root_ui.modal_focus_widget = self
        if self.misc_bindings[BindingName.GAIN_FOCUS]:
            self.misc_bindings[BindingName.GAIN_FOCUS]()

    ###################################################################################
    def loseFocus(self):
        """This widget has lost focus"""
        if self.root_ui.modal_focus:
            self.root_ui.modal_focus = None
            self.root_ui.modal_focus_widget = None
        if self.misc_bindings[BindingName.LOSE_FOCUS]:
            self.misc_bindings[BindingName.LOSE_FOCUS]()

    ###################################################################################
    def draw(self) -> None:
        """Draw the Widget"""
        if not self._laid_out:
            self.layout()
        if self._border_window:
            if self.focus:
                self._border_window.border(0, 0, 0, 0, "*")
            else:
                self._border_window.border()

    ###################################################################################
    def handle_keyboard_input(self, key: Keys) -> bool:
        """Handle character input - return if event handled"""
        self.debug(f"handle_keyboard_input({key=}) {self.bindings}")
        if key in self.bindings:
            self.bindings[key]()
            return True
        self.debug(f"Not handled: {self.bindings}")
        return False

    ###################################################################################
    def assign_name(self) -> str:
        """Assign a name if one isn't given"""
        return self.__class__.__name__

    ###################################################################################
    def add(self, widget: Self, name: str = "") -> Widget:
        """Add a subwidget - for containers"""
        raise AttributeError("Only containers can add subwidgets")

    ###################################################################################
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"

    ###################################################################################
    def set_parent(self, window: curses.window):
        """Set the parent"""
        self._parent_window = window

    ###################################################################################
    def handle_mouse_event(self, x: int, y: int, bstate: int) -> None:
        """Hande mouse input"""
        # mouse event, represented as a 5-tuple (id, x, y, z, bstate)
        if not self.mouse_bindings:
            return None
        for binding, callback in self.mouse_bindings.items():
            if binding & bstate:
                return callback(x, y, bstate)
        return None


# EOF
