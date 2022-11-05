import os
import sys
import time
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
from O_cs_rv3 import *
import O_cs_rv3 as csr

erstellenbool = False
bid_num = []
log_Path_img = [None]
log_user_gui = []
log_user_lusd = []
log_user_sqlite = []
image_shueler = []
kopie_schueler = []
submit_schueler = []
pathCSVFileStorage = [None]

class CSVUploadWindow(QWidget):
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi('GUI\CSV_Upload.ui', self)
            self.pushButton.clicked.connect(self.csv_upload)
            self.pushButton_2.clicked.connect(self.browserWindowOpen)
            self.diaolog = DialogDone()
            self.diaError = DialogImpError()
            try:
                element = pathCSVFileStorage[-1]
                self.label_3.setText(element)
            except:
                self.label_3.setText("")
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (Class:CSVUploadWindow())\n")
                log.close()

    def browserWindowOpen(self):
        try:
            self.browser_window = BrowserWindow()
            self.browser_window.show()
            self.close()
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (browserWindowOpen())\n")
                log.close()

    def pbar(self):
        k = 500
        for i in range(k):
            self.progressBar.setValue(i)
            time.sleep(0.1)

    def csv_upload(self):
        try:
            filename = pathCSVFileStorage[-1]
            with open(filename, encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    print(row)
                    csr.SchuelerErstellen("aktiv",row['Klassen_Klassenbezeichnung'],None,row['Schueler_Nachname'],row['Schueler_Vorname'],row['Schueler_Geburtsdatum'])
                file.close()
            with open("ImHis.txt", "a") as imhis:
                history = date.today()
                imhis.write(str(history) + "\n")
                imhis.close()
            self.close()
            self.diaolog.show()
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Es ist etwas schief gelaufen beim erstellen der Schüler\n")
                log.close()

class BrowserWindow(QWidget):
    def __init__(self):
        try:
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
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (Class: BrowserWindow())\n")
                log.close()
    def getPath(self):
        try:
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
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (getPath())\n")
                log.close()

    def confirm(self):
        try:
            self.windowCSVUpload = CSVUploadWindow()
            self.windowCSVUpload.show()
            self.close()
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (confirm())\n")
                log.close()

    def cancel(self):
        try:
            self.windowCSVUpload = CSVUploadWindow()
            self.windowCSVUpload.show()
            self.close()
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (cancel())\n\n")
                log.close()

class DialogDone(QDialog):
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi("GUI\progess.ui", self)
            self.label.setText("Import ist Fertig!")
            self.pushButton.clicked.connect(self.pressed)
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (Class: DialogDone())\n")
                log.close()

    def pressed(self):
        self.close()

class DialogImpError(QDialog):
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi("GUI\progess.ui", self)
            self.label.setText("Error: Import konnte nicht erfolgreich abgeschlossen werden!")
            self.pushButton.clicked.connect(self.pressed)
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (Class: DialogImpError())\n")
                log.close()

    def pressed(self):
        self.close()

class DialogWindow(QDialog):
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi("GUI\progess.ui", self)
            self.label.setText("Update: Datenbank neu erstellen!")
            self.pushButton.clicked.connect(self.pressed)
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (DialogWindow())\n")
                log.close()

    def pressed(self):
        self.close()

class MainWindow(QWidget):
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi('GUI\GUI.ui', self)
            self.schuelerCount()
            self.setAcceptDrops(False)
            csr.KlassenHinzufuegen()
            self.show_logWin()
            title = "Ausweis Verwaltung"
            self.dialo = DialogWindow()
            self.UpladWin = CSVUploadWindow()
            self.historyimp()
            self.pushButton.clicked.connect(self.changePhoto)
            self.pushButton_2.clicked.connect(self.del_schueler)
            self.pushButton_3.clicked.connect(self.erstellen)
            self.pushButton_5.clicked.connect(self.schueler_suche)
            self.pushButton_7.clicked.connect(self.del_img)
            self.pushButton_10.clicked.connect(self.show_db)
            self.treeView.clicked.connect(self.getPath)
            self.pushButton_4.clicked.connect(self.openUpload)
            self.dialo.show()
            self.paths()
            self.photoViewer = self.label_7
            auto_names = ["10LH-1","13LH-1","10BV01","10BV02"
            ,"10PS01","10PS02","10KFZ1","10KFZ2"
            ,"10KFZ3","10PA1","10PA2","10MR-0"
            ,"10ASH1","10ASH2","10MBX0"
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
            self.lineEdit_7.setCompleter(completer)
            self.tableWidget.cellClicked.connect(self.cell_row_print)
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("#####################")
                log.write("Error: (MainWindow())\n")
                log.close()

    def historyimp(self):
        try:
            with open("ImHis.txt", "r") as imhis:
                for i in imhis:
                    self.label_16.setText("Letzter Import:" + i )
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (historyimp())\n")
                log.close()

    def cell_row_print(self):
        try:
            data = []
            column = self.tableWidget.currentRow()
            self.tableWidget.selectRow(column)

            if (os.path.exists("temp.jpg")):
                os.remove("temp.jpg")

            try:
                for i in range(5):
                    self.QTableWidgetItem = self.tableWidget.selectedItems()[i]
                    data.append(self.QTableWidgetItem.text())
                self.lineEdit.setText(data[0])
                self.lineEdit_2.setText(data[1])
                self.lineEdit_3.setText(data[2])
                self.lineEdit_4.setText(data[3])
                connection = sqlite3.connect('schuelerausweis.sqlite')
                connection.row_factory = lambda cursor, row: row[0]
                cursor = connection.cursor()
                cursor.execute("SELECT foto FROM schueler WHERE vorname=? AND nachname=?", (data[0],data[1],))
                photo = cursor.fetchone()
                if (photo == None):
                    self.set_image("Avatar.jpg")
                else:
                    csr.SchuelerErstellen.writeBinarytoFile(photo,"temp.jpg")
                    self.set_image("temp.jpg")
                cursor.close()
            except:
                self.label_12.setText("Keine Daten in der Tabelle vorhanden")
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (cell_row_print())\n")
                log.close()

    def del_img(self):
        try:
            csr.SchuelerBildDel(self.lineEdit.text(),self.lineEdit_2.text(),self.lineEdit_3.text())
            pixmap = QPixmap("Avatar.jpg")
            small_pixmap = pixmap.scaled(281, 321)
            pix = self.photoViewer.setPixmap(small_pixmap)
            log_Path_img.append("Avatar.jpg")
            self.schueler_suche()
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (del_img())\n")
                log.close()

    def del_schueler(self):
        try:
            csr.SchuelerLoeschen(self.lineEdit.text(),self.lineEdit_2.text(),self.lineEdit_3.text())
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.schueler_suche()
            self.show_logWin()
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (del_schueler())\n")
                log.close()

    def paths(self):
        try:
            dir_path = self.lineEdit_6.text()
            model = QFileSystemModel()
            model.setRootPath(dir_path)
            model.setNameFilters(["*.jpg","*.png"])
            model.setNameFilterDisables(False)
            tree = self.treeView
            tree.setAnimated(True)
            tree.setSortingEnabled(True)
            tree.setModel(model)
            tree.setRootIndex(model.index(dir_path))
            tree.setDragEnabled(True)
            tree.hideColumn(1)
            tree.hideColumn(2)
            tree.hideColumn(3)
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (paths())\n")
                log.close()

    def getPath(self):
        try:
            for ix in self.treeView.selectedIndexes():
                model = QFileSystemModel()
                pathCSVFile = model.filePath(ix)
                self.label_14.setText(log_Path_img[-1])
                try:
                    log_Path_img.pop(0)
                except:
                    with open("log/log_create_schueler.txt", "a") as logfile:
                        logfile.write("Erorr: (getPath)\n")
                        logfile.close()

                finally:
                    log_Path_img.append(pathCSVFile)
                    self.set_image(log_Path_img[-1])
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (getPath())\n")
                log.close()

    def erstellen(self):
        try:
            vorname = self.lineEdit.text()
            nachname = self.lineEdit_2.text()
            gebdat = self.lineEdit_3.text()
            gebdat = gebdat.replace(".","-")
            klasse = self.lineEdit_4.text()
            self.lineEdit_7.setText(klasse)
            status = self.lineEdit_5.text()
            foto = log_Path_img[-1]
            csr.SchuelerErstellen(status,klasse,foto,nachname,vorname,gebdat)
            self.schuelerCount()
            self.schueler_suche()
            self.show_logWin()
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (erstellen())\n")
                log.close()

    def clicked_search(self):
        try:
            for n in range(40):
                for m in Range(4):
                    self.tableWidget.setItem(n,m, QTableWidgetItem)
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (clicked_search())\n")
                log.close()

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
            log_Path_img.append(file_path)
            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        try:
            pixmap = QPixmap(file_path)
            small_pixmap = pixmap.scaled(281, 321)
            pix = self.photoViewer.setPixmap(small_pixmap)
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (set_image())\n")
                log.close()

    def schueler_suche(self):
        try:
            self.tableWidget.clear()
            kid = self.lineEdit_7.text()
            name = self.lineEdit_8.text()
            self.tableWidget.setHorizontalHeaderLabels(["Vorname","Nachname","Geburtstag","Klasse","Gültigbis","Foto", "Status"])
            self.label_12.setText("")
            box_klasse = self.checkBox.isChecked()
            box_name = self.checkBox_2.isChecked()
            self.show_logWin()




            if (box_klasse == True):
                results = csr.SucheKlasse.suche_klasse(kid)
                for n, key in enumerate(results):
                    if(key[5]==None):
                        l = list(key)
                        l[5] = "None"
                        key = tuple(l)
                    else:
                        l = list(key)
                        l[5] = "Vorhanden"
                        key = tuple(l)
                    for m, item in enumerate(key):
                        self.tableWidget.setItem(n,m, QTableWidgetItem(item))
            elif (box_name == True):
                results = csr.SucheKlasse.suche_name(name)
                for n, key in enumerate(results):
                    if(key[5]==None):
                        l = list(key)
                        l[5] = "None"
                        key = tuple(l)
                    else:
                        l = list(key)
                        l[5] = "Vorhanden"
                        key = tuple(l)
                    for m, item in enumerate(key):
                        self.tableWidget.setItem(n,m, QTableWidgetItem(item))
            elif (box_name == True and box_klasse == True):
                results = csr.SucheKlasse.suchen(name,kid)
                for n, key in enumerate(results):
                    if(key[5]==None):
                        l = list(key)
                        l[5] = "None"
                        key = tuple(l)
                    else:
                        l = list(key)
                        l[5] = "Vorhanden"
                        key = tuple(l)
                    for m, item in enumerate(key):
                        self.tableWidget.setItem(n,m, QTableWidgetItem(item))
        except:
            self.label_6.setText("Klasse nicht gefunde/Error")
            with open("log/log_create_schueler.txt", "a") as logfile:
                logfile.write("Klasse nicht gefunden/Error F(schueler_suche())\n")
                logfile.close()

    def show_db(self):
        try:
            sql_DB = "schuelerausweis.sqlite"
            sql = "SELECT * FROM schueler"
            connection = sqlite3.connect(sql_DB)
            cursor = connection.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            print(results)
            cursor.close()
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (show_db())\n")
                log.close()

    def changePhoto(self):
        try:
            path = log_Path_img[-1]
            print(path)
            csr.AddPhoto(path,self.lineEdit.text(), self.lineEdit_2.text(),self.lineEdit_3.text())
            self.schueler_suche()
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (changePhoto())\n)")
                log.close()

    def schuelerCount(self):
        try:
            sql_DB = "schuelerausweis.sqlite"
            connection = sqlite3.connect(sql_DB)
            cursor = connection.cursor()
            cursor.execute("SELECT bid FROM schueler")
            results = cursor.fetchall()
            count = 0
            for i in results:
                count+=1
            connection.commit()
            cursor.close()
            self.label_15.setText("Schüler in der Datenbank: " + str(count))
        except:
            with open("log/log_create_schueler.txt", "a") as logfile:
                logfile.write("Error: (schuelerCount)/Keine Schüler in der Datenbank\n")
                logfile.close()

    def openUpload(self):
        try:
            self.UpladWin.show()
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (openUpload())\n")
                log.close()

    def show_logWin(self):
        try:
            self.listWidget.clear()
            with open("log/log_create_schueler.txt", "r") as logfile:
                for i in logfile:
                    self.listWidget.addItem(i)
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (show_logWin())\n")
                log.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = MainWindow()
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')
