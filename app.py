from random import choices
from Ui_window import Ui_MainWindow
import sys

from PyQt5.QtGui import QPixmap,QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox

import win32ui

def openfile():
    exists = "图片文件 (*.jpg,jpeg,png,bmp)|*.jpg;*.jpeg;*.png;*.bmp|视频文件 (*.mp4,gif,wmv,avi)|*.mp4;*.gif;*.wmv;*.avi|所有文件 (*.*)|*.*|| "
    dlg = win32ui.CreateFileDialog(True, "txt", None, 0x04 | 0x02,exists)
    dlg.DoModal()
    result = dlg.GetPathName()
    return result

movie = ['mp4','gif','wmv','avi']
picture = ['jpg','jpeg','png','bmp']

class UWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        self.hasmovie = False

        QMainWindow.__init__(self,parent)

        self.setupUi(self)

        self.playButton.clicked.connect(self.process_playmovie_do)
        self.stopButton.clicked.connect(self.process_stopmovie_do)
        self.openButton.clicked.connect(self.process_open_do)
        self.actionOpen.triggered.connect(self.process_open_do)
        self.actionExit.triggered.connect(self.process_exit)
        self.actionPlay.triggered.connect(self.process_playmovie_do)
        self.actionStop.triggered.connect(self.process_stopmovie_do)

    def process_playmovie_do(self):
        if self.hasmovie:
            self.movie.start()
        else:
            reply = QMessageBox.critical(self,'错误','您没有选择或选择的不是视频文件！', QMessageBox.Retry)
            self.process_open_do()
            return
    
    def process_stopmovie_do(self):
        if self.hasmovie:
            self.movie.stop()
        else:
            reply = QMessageBox.critical(self,'错误','您没有选择或选择的不是视频文件！', QMessageBox.Retry)
            self.process_open_do()
            return
    
    def process_open_do(self):
        self.choice = openfile()
        if self.choice == '':
            reply = QMessageBox.critical(self,'错误','您没有选择文件！', QMessageBox.Retry)
            self.process_open_do()
            return

        self.dirEdit.clear()
        self.dirEdit.setText(self.choice)
        self.choices = list(self.choice)
        if self.choices[-4] == "j" and self.choices[-5] == '.':
            filesuffix = self.choices[-4] + self.choices[-3] + self.choices[-2] + self.choices[-1]
        elif self.choices[-4] == ".":
            filesuffix = self.choices[-3] + self.choices[-2] + self.choices[-1]
        if filesuffix in picture:
            self.viewlabel.setScaledContents(False)
            self.viewlabel.setPixmap(QPixmap(self.choice))
        elif filesuffix in movie:
            self.hasmovie = True
            print(type(self.choice))
            self.movie = QMovie(self.choice)
            self.viewlabel.setMovie(self.movie)
        else:
            reply = QMessageBox.critical(self,'错误','您选择的不是媒体文件！', QMessageBox.Retry)
            self.process_open_do()
            return

    def process_exit(self):
        self.close()
        
def main():
    app = QApplication(sys.argv)
    hellowindow = UWindow()
    hellowindow.show()
    app.exec_()

if __name__ == "__main__":
    main()