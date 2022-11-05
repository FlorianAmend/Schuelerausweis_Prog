import os
import sys
from PyQt6 import QtWidgets
from PySide6 import *
import PySide6 as PySide6
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt as QtCore
from PyQt6 import uic


class DialogWindowError(QDialog):
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi("GUI\progess.ui", self)
            self.label.setText("Vorname,Nachname,Klasse oder Geburtstag fehlt!")
            self.pushButton.clicked.connect(self.pressed)
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (DialogWindow())\n")
                log.close()

    def pressed(self):
        self.close()
