"""Data about a sector"""

from typing import Self, Any

#######################################################################################
type opt_int = opt_int | None


#######################################################################################
#######################################################################################
#######################################################################################
class Sector:
    """A single sector"""

    def __init__(self, x: int, y: int, des: str, **kwargs):
        self._data = kwargs
        self._data.update({"x": x, "y": y, "des": des})

    def __getattr__(self, item):
        return self._data.get(item, None)

    def keys(self) -> list[str]:
        """Return all the keys"""
        return list(self._data.keys())

    def items(self) -> list[tuple[str, Any]]:
        """Return the dictionary items of the sector"""
        return list(self._data.items())

    def __getitem__(self, item):
        return self._data.get(item)

    def update(self, other: Self):
        """Update with details from another sector"""
        assert isinstance(other, Sector)
        assert other.x == self.x
        assert other.y == self.y
        for k, v in other.items():
            if v:
                self._data[k] = v


# EOF
