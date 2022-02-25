from PyQt5 import QtCore
from pynput.keyboard import Listener, Key, KeyCode

class KeyMonitor(QtCore.QObject):
    keyPressed = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.listener = Listener(on_release=self.on_release)

    def listener(self):
        return self.listener

    def on_release(self, key):
        if key == Key.print_screen:
            self.keyPressed.emit("print")
        elif key == Key.enter:
            self.keyPressed.emit("enter")
        elif key == Key.esc:
            self.keyPressed.emit("esc")

    def stop_monitoring(self):
        self.listener.stop()

    def start_monitoring(self):
        self.listener.start()