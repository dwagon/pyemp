"""Container of other widgets"""

from typing import Any, Generator

from .keys import Keys
from .widget import Widget


#######################################################################################
#######################################################################################
#######################################################################################
class Container(Widget):
    """Container of Widgets"""

    def __init__(
        self,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.bindings = {}
        self.bindings.update(kwargs.get("bindings", {}))

    ###################################################################################
    def children_widgets(self) -> Generator[Widget, None, None]:
        """Return all children widgets"""
        for _ in self.widget_tree.children(self.node_id):
            yield _.data

    ###################################################################################
    def layout(self):
        """Setup - outer canvas for borders,etc, inner canvas for widgets"""
        super().layout()
        for widget in self.children_widgets():
            widget.set_parent(self._window)
            widget.layout()

    ###################################################################################
    def add(self, widget: Widget, name: str = "") -> Widget:
        """Add a widget to the container"""
        name = widget.name if widget.name else name
        if not name:
            name = widget.assign_name()
        widget.name = name

        widget.root_ui = self.root_ui
        node = self.widget_tree.create_node(tag=name, data=widget, parent=self.node_id)
        widget.node_id = node.identifier
        return widget

    ###################################################################################
    @property
    def required_height(self) -> int:
        """required_height of container"""
        if children := list(self.children_widgets()):
            h = max(_.required_height for _ in children)
        else:
            h = 1  # Min size
        return h

    ###################################################################################
    @property
    def required_width(self) -> int:
        """required_width of container"""
        if children := list(self.children_widgets()):
            w = max(_.required_width for _ in children)
        else:
            w = 1  # Min size
        return w

    ###################################################################################
    def draw(self):
        """Draw the window"""
        super().draw()
        for widget in self.children_widgets():
            widget.draw()

    ###################################################################################
    def handle_keyboard_input(self, key: Keys) -> bool:
        """Handle character input"""

        if key in self.bindings:
            self.debug(f"{self.name} handle_keyboard_input({key=})")
            self.bindings[key]()
            return True
        return False


# EOF
