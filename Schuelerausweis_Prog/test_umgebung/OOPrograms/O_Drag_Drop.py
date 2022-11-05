import os
import sys
from PyQt6 import QtWidgets
from PySide6 import *
import PySide6 as PySide6
from PyQt6.QtGui import *
from PyQt6.QtGui import QFileSystemModel, QPixmap
import PyQt6.QtGui as QtG
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QTreeView, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt
from PyQt6 import uic

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        #self.setAlignment(Qt.Alignment.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setStyleSheet('''
        QLabel{
            border: 4px dashed #aaa
        }

        ''')

    def setPixmap(self, image):
        super().setPixmap(image)

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400,400)
        self.setAcceptDrops(True)

        mainLayout = QVBoxLayout()

        self.photoViewer = ImageLabel()
        mainLayout.addWidget(self.photoViewer)

        self.setLayout(mainLayout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            #event.setDropAction(QtG.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path)

            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        self.photoViewer.setPixmap(QPixmap(file_path))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = AppDemo()
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')
