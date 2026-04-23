"""Communications with the server"""

import socket
import select
from typing import Generator

type emp_sock = Generator[str, str, None]


#######################################################################################
def setup_socket(server: str = "localhost", port: int = 6665) -> emp_sock:
    """Return a socket for comms"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server, port))
        while True:
            select.select([sock], [], [])
            data = sock.recv(1024 * 5)
            print(f"DBG {len(data)=}")
            msg = yield data.decode("utf-8").strip()
            sock.send((msg + "\n").encode("utf-8"))


# EOF
