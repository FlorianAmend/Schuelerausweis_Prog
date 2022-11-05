import sqlite3
from tkinter import messagebox
import os.path
from os import path


log = open("log\log_DB.txt", "a")


class Create_Database:
    def __init__(self):
        self.Create_db()

    def Create_db(self):
        if(path.exists("schuelerausweis.sqlite") == True):
            pass
        else:
            #######################################################
            #Creating a Connection to the Database
            connection = sqlite3.connect('schuelerausweis.sqlite')
            #Setting the I/O cummunication with the Database up
            cursor = connection.cursor()
            log.write("Erstellen der Datenbank\n")
            #######################################################
                #######################################################
            #Creating the Tables
            table_klasse = """CREATE TABLE IF NOT EXISTS klasse(kid STRING PRIMARY KEY, dauer INT)"""
            table_schueler = """CREATE TABLE IF NOT EXISTS schueler(sid INT AUTO_INCREMENT, bid INT PRIMARY KEY, status STRING, kid STRING, foto BLOB, auswname STRING, nachname STRING, auswvname STRING, vorname STRING, gebdat DATE, einschulung DATE, gültigbis DATE, FOREIGN KEY(kid) REFERENCES klasse(kid))"""
            #NICE TO HAVE
            #table_lehrer = """CREATE TABLE IF NOT EXISTS lehrer(lid PRIMARY KEY, kid STRING, nachname STRING, foto BLOB, FORGEIGN KEY(kid) REFERENCES klasse(kid))"""
            #Creating Tables done
            ######################################################

            ######################################################
            #Execution for creating Tables
            cursor.execute(table_klasse)
            cursor.execute(table_schueler)
            log.write("Erstellen der Tables (Klasse und Schueler)\n")
            #Execution for creating Tables done
            ######################################################

            ######################################################
            #Saving everything that was created in the Database
            connection.commit()
            #Closing the Connection to the Database
            cursor.close()
            log.write("Closing Database\n")
            #####################################################

            log.write("Datenbank konnte nicht erstellt werden...\n")

Create_Database()
