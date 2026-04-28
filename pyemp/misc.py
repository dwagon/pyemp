"""Misc commands"""

from comms import emp_sock
from pyemp.commands import cmd_vers, cmd_dump, cmd_bmap
from pyemp.sector import Sector
from pyemp.map_data import MapData


#######################################################################################
def login(sock: emp_sock, country_name: str, password: str) -> None:
    """Login to a country"""
    sock.send("coun " + country_name)
    sock.send("pass " + password)
    sock.send("play")


###################################################################################
def initial_map_data(sock: emp_sock, config: dict[str, int | str]) -> MapData:
    """Login and get an initial dump"""
    login(sock, config["country"], config["password"])
    m = MapData()
    m.update(cmd_dump(sock))
    m.update(cmd_bmap(sock))
    vers_config = cmd_vers(sock)
    for var in ("WORLD_X", "WORLD_Y"):
        config[var] = vers_config[var]
    m.update(fill_map(config["WORLD_X"], config["WORLD_Y"]))
    return m


###################################################################################
def fill_map(max_x: int, max_y: int) -> MapData:
    """Fill the empty spots of the map in"""
    m = MapData()
    for x in range(-max_x // 2, max_x // 2):
        for y in range(-max_y // 2, max_y // 2):
            m.add(Sector(x, y, ""))
    return m
