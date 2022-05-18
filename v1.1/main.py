
from tkinter import Frame
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget
from PyQt5.QtWidgets import QApplication, QSizePolicy, QGridLayout
from PyQt5.QtCore import QTimer, QRect, Qt
from PyQt5.QtGui import QPixmap, QImage
import sys
import cv2
from arayuz import Ui_MainWindow


class islem(QMainWindow):
    testaasd = 12
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.btnBaslat.clicked.connect(self.baslatVideo)
        self.ui.btnKapat.clicked.connect(app.exit)
        self.ui.btnGoruntuKaydet.clicked.connect(self.ekranKayit)
        
    
    def baslatVideo(self):
        self.startVideo()
    def ekranKayit(self):
        _,frame = self.cap.read()
        cv2.imwrite('ekranGoruntusu.jpg',frame)
                 
     
    def startVideo(self):
            self.cap = cv2.VideoCapture("testGoruntuArac.mp4")
            fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            self.timer = QTimer()
            millisecs = int(1000.0 / fps)
            self.timer.setTimerType(Qt.PreciseTimer)
            self.timer.timeout.connect(self.nextFrameSlot)
            self.timer.start(millisecs)

    def nextFrameSlot(self):
        ret, frame = self.cap.read()
        if ret == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pix = QPixmap.fromImage(img)
            pix = pix.scaled(self.ui.lblVid.width(), self.ui.lblVid.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.ui.lblVid.setPixmap(pix)





if __name__ == "__main__":
    import sys
    app = QApplication([])
    MainWindow = islem()
    MainWindow.show()
    sys.exit(app.exec_())

"""
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = islemler()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
"""