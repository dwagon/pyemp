"""Communications with the server"""

import socket
import select
from enum import StrEnum
from typing import Generator

type emp_sock = Generator[list[str], str, None]


class EmpProto(StrEnum):
    """Empire protocol values"""

    C_CMDOK = "0"
    C_DATA = "1"
    C_INIT = "2"
    C_EXIT = "3"
    C_FLUSH = "4"
    C_NOECHO = "5"
    C_PROMPT = "6"
    C_ABORT = "7"
    C_REDIR = "8"
    C_PIPE = "9"
    C_CMDERR = "A"
    C_BADCMD = "B"
    C_EXECUTE = "C"
    C_FLASH = "D"
    C_INFORM = "E"
    C_LAST = "E"


#######################################################################################
def setup_socket(server: str = "localhost", port: int = 6665) -> emp_sock:
    """Return a socket for comms"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server, port))
        while True:
            result = []
            while True:
                select.select([sock], [], [])
                recvd_text = sock.recv(1024 * 4).decode("utf-8")
                lines = recvd_text.splitlines()
                for line in lines:
                    status, text = line.split(None, 1)
                    result.append(text)
                if status == EmpProto.C_DATA:
                    continue
                break
            msg = yield result
            sock.send((msg + "\n").encode("utf-8"))


# EOF
