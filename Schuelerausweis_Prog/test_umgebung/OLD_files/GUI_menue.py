import os
import sys
import time
import csv
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
import O_cs_rv3 as csr



pathCSVFileStorage = [None]

class DialogWindow(QDialog):
    def __init__(self,text):
        super().__init__()
        uic.loadUi("GUI\progess.ui", self)
        self.label.setText(text)
        self.pushButton.clicked.connect(self.pressed)

    def pressed(self):
        self.close()

class FotoListe(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI\liste_photo.ui', self)
        auto_names = ["10LH-1","13LH-1"
        ,"10BV01","10BV02"
        ,"10PS01","10PS02","10KFZ1","10KFZ2"
        ,"10KFZ3","10PA1","10PA2","10MR-0","10ASH1","10ASH2","10MBX0"
        ,"10EAX0","10EEX0","10EG01","10EG02"
        ,"10BZX1","10BZX2","10ITS1","10ITS2"
        ,"10ITS3","10ME-0","10TIX0","10TZX1"
        ,"10TZX2","10IMX0","10ZMX0","11IMX1"
        ,"11IMX2","11WMX0","11ZMX0","11BGX1"
        ,"11FOX2","11FOX1","11FOI0","11BZX0","11FKMO","11ITS1"
        ,"11ITS2","11ITS3","11ME-0","11PDX0"
        ,"11TIX0","11EAX0","11EEX0","11EG-0","11KL-0","11MB-0"
        ,"11FL-0","11ZI-1","11ZI-2","11ASH1"
        ,"11ASH2","11KFZ1","11KFZ2","11KFZ3"
        ,"11PAB0","11SPX1","11SPX2",
        "11BFI0","11BGX2","11BGX3"
        ,"11BFE0","11BFF0","11BFH0","12BGPI"
        ,"12BGME","12BFI0",
        "12ASH1","12ASH2","12KFZ1","12KFZ2"
        ,"12KFZ3","12KL-1","12PAB1","12PAB2"
        ,"12SPX1","12SPX2","12FL-1","12ZI01"
        ,"12ZI02","12MB-1","12EEX0","12EG01"
        ,"12EG02","12BZX0","12ITS1","12ITS2"
        ,"12ITS3","12ME-0","12PDX0","12TIX1"
        ,"12TIX2","12FOX1","12FOX2","12FOB0"
        ,"12FOM0","12BGB0","12IMX1","12IMX2"
        ,"12WMX0","12ZMX0","13IMX1","13IMX2"
        ,"13ZMX0","13ME-0","13SPX0","13EAX0"
        ,"13EEX0","13EG01","13MB-0","13ASH1"
        ,"13ASH2","13KFZ1","13KFZ2","13KL-0"
        ,"13BGME","13BGPI","10BJH0",
        "01FSHK","02FSHK","10BVP1","10BVP2",
        "08MS-0","09MS-0","10MS-0",
        "10BFX1","10BFX2","10BFX4","10BFX3",
        "11LH01","11LH02","12LH01","12LH02",
        "10INT1","10INT2","10INT3"]
        completer = QCompleter(auto_names)
        self.lineEdit.setCompleter(completer)
        self.pushButton_2.clicked.connect(self.klasseSuchen)
        self.pushButton_3.clicked.connect(self.clearWindow)

    def clearWindow(self):
        self.tableWidget.clear()

    def klasseSuchen(self):
        self.tableWidget.clear()
        kid = self.lineEdit.text()

        try:
            results = csr.SucheKlasse.suche_klasse(kid)
            for n, key in enumerate(results):
                for m, item in enumerate(key):
                    self.tableWidget.setItem(n,m, QTableWidgetItem(item))
        except:
            self.label_2.setText("Klasse nicht gefunden")

class MenueWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI\menue.ui', self)
        self.listphoto = FotoListe()
        self.csv_up_op = CSVUploadWindow()
        self.pushButton.clicked.connect(self.open_csv_window)
        self.pushButton_3.clicked.connect(self.openFotolist)

    def open_csv_window(self):
        self.csv_up_op.show()

    def openFotolist(self):
        self.listphoto.show()

class CSVUploadWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI\CSV_Upload.ui', self)
        self.pushButton.clicked.connect(self.csv_upload)
        self.pushButton_2.clicked.connect(self.browserWindowOpen)
        try:
            element = pathCSVFileStorage[-1]
            self.label_3.setText(element)
        except:
            self.label_3.setText("")

    def browserWindowOpen(self):
        self.browser_window = BrowserWindow()
        self.browser_window.show()
        self.close()

    def pbar(self):
        k = 500
        for i in range(k):
            self.progressBar.setValue(i)
            time.sleep(0.1)
            #####Baustell
    def csv_upload(self):
        try:
            filename = pathCSVFileStorage[-1]
            with open(filename, encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    csr.SchuelerErstellen("aktiv",row['Klassen_Klassenbezeichnung'],None,row['Schueler_Nachname'],row['Schueler_Vorname'],row['Schueler_Geburtsdatum'])
                    file.close()
                    guiprog.show_logWin()
        except:
            self.dioWin = DialogWindow("Leider ist etwas schief gelaufen. Bitte versuchen Sie den Import noch einmal")
            self.dioWin.show()
            #####Baustell ende

class BrowserWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI\FileBrowser.ui', self)
        self.treeView.clicked.connect(self.getPath)
        self.pushButton.clicked.connect(self.confirm)
        self.pushButton_2.clicked.connect(self.cancel)
        dir_path = ""
        tree = self.treeView
        model = QFileSystemModel(self.treeView)
        model.setRootPath(dir_path)
        model.setNameFilters(["*.csv"])
        model.setNameFilterDisables(False)
        tree.setAnimated(True)
        tree.setSortingEnabled(True)
        tree.setModel(model)
        tree.setRootIndex(model.index(dir_path))
        tree.hideColumn(1)
        tree.hideColumn(2)
        tree.hideColumn(3)

    def getPath(self):
        item = []
        for ix in self.treeView.selectedIndexes():
            try:
                item.pop(0)
            except:
                pass
            model = QFileSystemModel()
            pathCSVFile = model.filePath(ix)
            item.append(pathCSVFile)
            pathCSVFileStorage.append(pathCSVFile)
            self.label_2.setText(pathCSVFile)

    def confirm(self):
        self.windowCSVUpload = CSVUploadWindow()
        self.windowCSVUpload.show()
        self.close()

    def cancel(self):
        self.windowCSVUpload = CSVUploadWindow()
        self.windowCSVUpload.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = MainWindow()
    myApp.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')
