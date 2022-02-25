import socket
import sys

from meowshot import MeowShot
from server import Server
from PyQt5.QtWidgets import QApplication

def create_socket():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

def get_lock(process_name):
    sock = create_socket()
    try:
        sock.bind('\0' + process_name)
        return sock
    except socket.error:
        return None

if __name__ == "__main__":
    process_name = "meowshot"
    lock = get_lock(process_name)

    if lock is not None:
        app = QApplication(sys.argv)
        meow = MeowShot()
        server = Server(meow, lock)
        server.listen_async()
        app.exec_()
    else:
        print("Process already running, sending 'take_screenshot' signal.")
        lock = create_socket()
        lock.connect('\0' + process_name)
        lock.send(b'take_screenshot')