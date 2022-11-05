import sys
import subprocess

#This file is to install all the missing libraries needed for this program to work.

log = open("log\log_Package.txt", "a")

packages = ["PyQt6","sqlite3", "base64", "PyQt6-tools", "PySide6","python-dateutil"]

package_num = 0

class Install():
    def __init__(self):
        self.install_pyqt6()

    def install_pyqt6(self):
        try:
            for package in packages:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                log.write(package + " Wurde installiert\n")
        except:
            log.write(package + " konnte nicht installiert werden.\n")


Install()
