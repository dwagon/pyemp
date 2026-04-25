"""Structure containing all the map data"""

from typing import Self
from pyemp.sector import Sector


#######################################################################################
#######################################################################################
#######################################################################################
class MapData:
    """All the map"""

    def __init__(self):
        self.data: dict[tuple[int, int], Sector] = {}

    def update(self, other: Self) -> None:
        """Update the data with another source"""
        assert isinstance(other, MapData)

        for coord in other.data:
            if coord not in self.data:  # No self data so we take new one
                self.data[coord] = other.data[coord]
                continue
            self.data[coord].update(other.data[coord])

    def add(self, sect: Sector) -> None:
        """Add a sector to the map"""
        self.data[(sect.x, sect.y)] = sect

    def __getitem__(self, item):
        return self.data[item]

    def __contains__(self, item):
        if item in self.data:
            return True
        return False

    def _map_range(self) -> tuple[tuple[int, int], tuple[int, int]]:
        min_x = min_y = 9999
        max_x = max_y = -9999
        for x, y in self.data:
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
    def draw(self, draw_scale=True) -> str:
        """Return a picture of the map"""
        ans = []
        border = 4
        (min_x, min_y), (max_x, max_y) = self._map_range()
        if draw_scale:
            ans.extend(self.draw_x_border(border))
        for y in range(
            min_y - border,
            max_y + border + 1,
        ):
            if draw_scale:
                ans.append(f"{y:3}  ")
            for x in range(min_x - border, max_x + border + 1):
                if _is_odd(x) != _is_odd(y):
                    ans.append(" ")
                    continue
                if (x, y) not in self.data:
                    ans.append(" ")
                else:
                    if self.data[x, y].des:
                        ans.append(self.data[x, y].des)
                    else:
                        ans.append(" ")
            if draw_scale:
                ans.append(f" {y:-3}\n")
        if draw_scale:
            ans.extend(self.draw_x_border(border))

        return "".join(ans)


#######################################################################################
def _is_odd(x: int) -> bool:
    if x % 2 == 1:
        return True
    return False


# EOF
