"""Curses exceptions"""


class ScreenTooSmall(Exception):
    """Screen is too small for widget"""

    def __init__(self, name: str, requested: int, maximum: int):
        self.name = name
        self.requested = requested
        self.maximum = maximum
        super().__init__(repr(self))

    def __repr__(self) -> str:
        return (
            f"<Screen Too Small: {self.name}: "
            f"requested = {self.requested} maximum = {self.maximum}>"
        )


# EOF
