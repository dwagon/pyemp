"""Handle vers output"""

from typing import Any
import re
from pyemp.comms import emp_sock


#######################################################################################
def cmd_vers(sock: emp_sock) -> dict[str, Any]:
    """Parse the vers command"""
    # Add more understanding of output when required
    config = {}
    msg = sock.send("vers")
    for line in msg:
        # World size is 64 by 32.
        if m := re.match(r"World size is (?P<x>\d+) by (?P<y>\d+).", line):
            config["WORLD_X"] = int(m.group("x"))
            config["WORLD_Y"] = int(m.group("y"))
    return config
