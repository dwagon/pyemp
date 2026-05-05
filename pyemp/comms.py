"""Communications with the server"""

import socket
import select
import time
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
            data = read_full(sock)
            lines = data.decode("utf-8").splitlines()
            result = []
            for line in lines:
                log(line)
                if len(line.split()) == 1:
                    status = line
                    text = ""
                else:
                    status, text = line.split(None, 1)
                if status != EmpProto.C_PROMPT:
                    result.append(text)
            msg = yield result
            log(msg)
            sock.send((msg + "\n").encode("utf-8"))


#######################################################################################
def log(msg: str) -> None:
    """Add something to the empire log"""
    with open("/tmp/empire_log", "a", encoding="utf-8") as logfh:
        print(f"{time.ctime()}: {msg}", file=logfh)


#######################################################################################
def read_full(sock) -> bytes:
    """Read a full result"""
    data = b""
    while select.select([sock], [], [], 0.1)[0]:
        recvd_data = sock.recv(1024 * 4)
        data += recvd_data
    return data


# EOF
