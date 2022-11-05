import os
import sys
from PyQt6 import QtWidgets
from PySide6 import *
import PySide6 as PySide6
from PyQt6.QtGui import *
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QTreeView, QListWidget, QListWidgetItem
from PyQt6.QtCore import QModelIndex
from PyQt6.QtCore import Qt as QtCore
from PyQt6 import uic


class FileSystemView(QWidget):
    def __init__(self, dir_path):
        super().__init__()

        appWidght = 800
        appHeight = 300

        self.setWindowTitle("File System Viewer")
        self.setGeometry(300,300, appWidght,appHeight)

        self.model = QFileSystemModel()
        self.model.setRootPath(dir_path)

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(dirPath))

        layout = QVBoxLayout()
        layout.addWidget(self.tree)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    dirPath = r'C:\Users\flori\Documents\GitHub'

    demo = FileSystemView(dirPath)
    demo.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')
