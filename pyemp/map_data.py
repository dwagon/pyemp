"""Structure containing all the map data"""

from typing import Self
from pyemp.sector import Sector


#######################################################################################
#######################################################################################
#######################################################################################
class MapData:
    """All the map"""

    def __init__(self):
        self._data: dict[tuple[int, int], Sector] = {}

    def update(self, other: Self) -> None:
        """Update the data with another source"""
        for element in other._data:
            self._data[element] = other._data[element]

    def add(self, sect: Sector) -> None:
        """Add a sector to the map"""
        self._data[(sect.x, sect.y)] = sect

    def __getitem__(self, item):
        return self._data[item]

    def _map_range(self) -> tuple[tuple[int, int], tuple[int, int]]:
        min_x = min_y = 9999
        max_x = max_y = -9999
        for x, y in self._data:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        return (min_x, min_y), (max_x, max_y)

    ###################################################################################
    def draw_x_border(self, border: int) -> list[str]:
        """Return the x number border"""
        (min_x, _), (max_x, _) = self._map_range()

        ans = []

        ans.append("     ")
        for x in range(min_x - border, max_x + border + 1):
            if -10 < x < 0:
                ans.append("-")
            else:
                ans.append(f"{abs(x) // 10}")
        ans.append("\n")

        ans.append("     ")
        for x in range(min_x - border, max_x + border + 1):
            ans.append(f"{abs(x) % 10}")
        ans.append("\n")
        return ans

    ###################################################################################
    def draw(self) -> str:
        """Return a picture of the map"""
        ans = []
        border = 4
        (min_x, min_y), (max_x, max_y) = self._map_range()
        ans.extend(self.draw_x_border(border))
        for y in range(
            min_y - border,
            max_y + border + 1,
        ):
            ans.append(f"{y:3}  ")
            for x in range(min_x - border, max_x + border + 1):
                if _is_odd(x) != _is_odd(y):
                    ans.append(" ")
                    continue
                if (x, y) not in self._data:
                    ans.append(" ")
                else:
                    ans.append(self._data[x, y].des)
            ans.append(f" {y:-3}\n")
        ans.extend(self.draw_x_border(border))

        return "".join(ans)


#######################################################################################
def _is_odd(x: int) -> bool:
    if x % 2 == 1:
        return True
    return False


# EOF
