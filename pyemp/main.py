"""Main"""

from pyemp.comms import setup_socket
from pyemp.misc import login
from pyemp.dump import dump
from pyemp.bmap import bmap
from pyemp.map_data import MapData

CONFIG = {"server": "localhost", "port": 6665, "country": "1", "password": "1"}
MAP = MapData()


#######################################################################################
def main():
    """Main"""
    sock = setup_socket(CONFIG["server"], CONFIG["port"])
    next(sock)
    login(sock, CONFIG["country"], CONFIG["password"])
    data = dump(sock)
    MAP.update(data)
    data = bmap(sock)
    MAP.update(data)
    print(MAP.draw())


#######################################################################################
if __name__ == "__main__":
    main()
