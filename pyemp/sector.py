"""Data about a sector"""

from typing import Self, Any

#######################################################################################
type opt_int = int | None

# See https://www.empire.cx/infopages/Sector-types.html
# BASICS                   INDUSTRIES                MILITARY / SCIENTIFIC
#  .  sea                   d  defense plant          t  technical center
#  ^  mountain              i  shell industry         f  fortress
#  s  sanctuary             m  mine                   r  research lab
#  \  wasteland             g  gold mine              n  nuclear plant
#  -  wilderness            h  harbor                 l  library/school
#  ~  plains                w  warehouse              e  enlistment center
#  c  capital/city          u  uranium mine           !  headquarters
#  p  park                  *  airfield
#                           a  agribusiness           FINANCIAL
#  COMMUNICATIONS           o  oil field              b  bank
#  +  highway               j  light manufacturing
#  )  radar installation    k  heavy manufacturing
#  #  bridge head           %  refinery
#  =  bridge span
#  @  bridge tower

DESIG_KEY_MAP = {
    ".": "sea",
    "^": "mountain",
    "s": "sanctuary",
    "\\": "wasteland",
    "-": "wilderness",
    "~": "plains",
    "c": "capital",
    "p": "park",
    "+": "highway",
    ")": "radar",
    "#": "bridge head",
    "=": "bridge span",
    "@": "bridge tower",
    "d": "defense plant",
    "i": "shell industry",
    "m": "mine",
    "g": "gold mine",
    "h": "harbor",
    "w": "warehouse",
    "u": "uranium mine",
    "*": "airfield",
    "a": "agribusiness",
    "o": "oil field",
    "j": "light manufacturing",
    "k": "heavy manufacturing",
    "%": "refinery",
    "t": "technical center",
    "f": "fortress",
    "r": "research lab",
    "n": "nuclear plant",
    "l": "library/school",
    "e": "enlistment center",
    "!": "headquarters",
    "b": "bank",
    "?": "unknown",
}


#######################################################################################
def desig_name(desig: str) -> str:
    """Return human name for designator"""
    return DESIG_KEY_MAP.get(desig, "ERR")


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
