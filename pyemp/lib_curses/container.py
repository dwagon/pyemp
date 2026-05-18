"""Modal Curses Popup"""

from typing import Any

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

        self._widgets: dict[str, Widget] = {}

    ###################################################################################
    def layout(self):
        """Setup - outer canvas for borders,etc, inner canvas for widgets"""
        super().layout()
        for widget in self._widgets.values():
            widget.parent = self.window
            widget.layout()

    ###################################################################################
    def add(self, name: str, widget: Widget) -> Widget:
        """Add a widget to the container"""
        self._widgets[name] = widget
        self._widgets[name].name = name
        return widget

    ###################################################################################
    def delete(self, name: str):
        """Remove a widget from the container"""
        del self._widgets[name]

    # ###################################################################################
    # def derwin(self, *args, **kwargs):
    #     """Pass a derwin() call to the parent window"""
    #     return self.window.derwin(*args, **kwargs)
    #
    # ###################################################################################
    # def getmaxyx(self) -> tuple[int, int]:
    #     """Return max y, max x of container"""
    #     return self.nlines, self.ncols

    ###################################################################################
    @property
    def height(self) -> int:
        """height of container"""
        h = max(_.height for _ in self._widgets.values())
        self.debug(f"{self} height={h}")
        return h

    ###################################################################################
    @property
    def width(self) -> int:
        """width of container"""
        w = max(_.width for _ in self._widgets.values())
        self.debug(f"{self} width={w}")
        return w

    ###################################################################################
    def draw(self):
        """Draw the window"""
        super().draw()
        for widget in self._widgets.values():
            widget.draw()


# EOF
