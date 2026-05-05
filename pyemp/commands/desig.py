"""Designate a sector"""

from pyemp.comms import emp_sock


#######################################################################################
def cmd_desig(
    sock: emp_sock, sector_x: int, sector_y: int, new_desig: str
) -> list[str]:
    """Send a desig command"""
    msg = sock.send(f"desig {sector_x},{sector_y} {new_desig}")
    return msg


# EOF
