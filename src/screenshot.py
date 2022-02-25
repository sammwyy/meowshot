import pyautogui
from PyQt5.QtWidgets import QApplication

class Screenshot:
    def copy(self):
        QApplication.clipboard().setPixmap(self.result.toqpixmap())

    def crop(self, begin, end):
        self.result = self.image.crop((begin.x(), begin.y(), end.x(), end.y()))

    def shot(self):
        self.image = pyautogui.screenshot()
        self.result = self.image.copy()