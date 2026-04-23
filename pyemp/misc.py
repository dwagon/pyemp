"""Misc commands"""

from comms import emp_sock


#######################################################################################
def login(sock: emp_sock, country_name: str, password: str) -> None:
    """Login to a country"""
    sock.send("coun " + country_name)
    sock.send("pass " + password)
    sock.send("play")
