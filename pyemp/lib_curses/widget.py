"""Parent class for widgets"""

from typing import Callable, Any, Self


#######################################################################################
#######################################################################################
#######################################################################################
class Widget:
    """Generic Widget Class"""

    def __init__(self, **kwargs: Any):
        self.begin_y = kwargs.get("begin_y")
        self.begin_x = kwargs.get("begin_x")
        self.root = kwargs.get("root")
        self.parent = kwargs.get("parent")
        if not self.root:
            self.root = self.parent
        self.bindings: dict[Any, Callable[[Self], None]] = {}

    def draw(self) -> None:
        """Draw the Widget"""
        raise NotImplementedError

    def handle_input(self, key: int) -> None:
        """Handle character input"""
        if key in self.bindings:
            return self.bindings[key](self)
        return None

    def has_finished(self) -> bool:
        """Has the widget finished doing its thing"""
        return False


# EOF
