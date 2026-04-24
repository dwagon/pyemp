"""Handle a bmap output"""

from pyemp.comms import emp_sock
from pyemp.map_data import MapData
from pyemp.sector import Sector


#######################################################################################
def cmd_bmap(sock: emp_sock) -> MapData:
    """Handle a bmap command"""
    data = MapData()
    msg = sock.send("bmap *")
    min_x, _ = get_x_range(msg)
    for line in msg[2:-2]:  # Top and bottom lines are border
        if len(line.split()) == 2:  # Ignore empty but for y coord lines
            continue
        y = int(line.split(None, 1)[0])
        left_index = len(line.split(None, 1)[0])
        right_index = len(line.rsplit(None, 1)[1])
        map_part = line[left_index + 1 : -right_index]
        for pos, ch in enumerate(map_part, start=min_x):
            if is_valid_coord(pos, y) and ch != " ":
                data.add(Sector(x=pos, y=y, des=ch, sdes=" "))
    return data


#######################################################################################
def get_y_range(msg: list[str]) -> tuple[int, int]:
    "Return the Y bounds of the map"
    lower_y = int(msg[2].split(None, 1)[0])
    upper_y = int(msg[-3].split(None, 1)[0])
    return lower_y, upper_y


#######################################################################################
def get_x_range(msg: list[str]) -> tuple[int, int]:
    """Return the X bounds of the map"""
    if msg[0][0] == "-":
        tens = 0
    else:
        tens = int(msg[0][0])
    units = int(msg[1][0])
    lower_x = tens * 10 + units
    if "-" in msg[0]:
        lower_x = -lower_x

    tens = int(msg[0][-1])
    units = int(msg[1][-1])
    upper_x = tens * 10 + units
    return lower_x, upper_x


#######################################################################################
def is_valid_coord(x: int, y: int) -> bool:
    """Is the x,y coord valid (i.e. both even or both odd)"""
    if x % 2 == 1 and y % 2 == 1:
        return True
    if x % 2 == 0 and y % 2 == 0:
        return True

    return False


# EOF
