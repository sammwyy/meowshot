from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor, QFontMetrics
from PyQt5.QtCore import Qt, QPoint, QRect
import sys

from keymonitor import KeyMonitor
from screenshot import Screenshot

class MeowShot(QMainWindow):
    def __init__(self):
        super(MeowShot, self).__init__()
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.keymonitor = KeyMonitor()
        self.keymonitor.keyPressed.connect(self.keyPressed)
        self.keymonitor.start_monitoring()

        self.screenshot = Screenshot()

        self.is_dragging = False
        self.is_active = False

        self.open_gui()

    def drawCenterText(self, painter, x, y, text):
        qf = QFontMetrics(painter.font())
        i = 0
        for line in text.splitlines():
            line_width = qf.width(line)
            line_height = qf.height()
            line_space = 5

            line_x = int(x - (line_width / 2))
            line_y = int(y + ((line_height + line_space) * i))
            painter.drawText(line_x, line_y, line)
            i += 1

    def paintEvent(self, event):
        image = QPainter(self)
        image.drawPixmap(self.rect(), self.screenshot.image.toqpixmap())
        
        background = QPainter(self)
        background_brush = QBrush(QColor(0, 0, 0, 100))
        background.setBrush(background_brush)
        background.drawRect(QRect(0, 0, self.screen().size().width(), self.screen().size().height()))

        selection_box = QPainter(self)
        selection_box_brush = QBrush(QColor(100, 10, 120, 30))  
        selection_box.setBrush(selection_box_brush)   
        selection_box.drawRect(QRect(self.begin, self.end))       

        text_x = self.screen().size().width() / 2
        text_y = 100
        text_brush = QBrush(QColor(255, 255, 255, 255))
        background.setBrush(text_brush)
        self.drawCenterText(background, text_x, text_y, "Click and drag to draw a selection box\nPress [enter] to save it\nOr press [esc] to cancel") 

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            self.end = event.pos()
        self.update()

    def mousePressEvent(self, e):
        self.is_dragging = True
        self.begin = e.pos()
        self.end = e.pos()
        self.update()

    def mouseReleaseEvent(self, e):
        self.is_dragging = False
        self.end = e.pos()
        self.update()

    def open_gui(self):
        self.begin = QPoint()
        self.end = QPoint()
        self.screenshot.shot()
        self.showFullScreen()
        self.is_active = True

    def close_gui(self):
        self.is_active = False
        self.is_dragging = False
        self.hide()
        self.close()
        sys.exit(0)

    def keyPressed(self, key):
        if key == "print" and not self.is_active:
            self.open_gui()
        elif key == "enter" and self.is_active:
            self.screenshot.crop(self.begin, self.end)
            self.screenshot.copy()
            self.close_gui()
        elif key == "esc" and self.is_active:
            self.close_gui()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    meow = MeowShot()
    sys.exit(app.exec_()) 