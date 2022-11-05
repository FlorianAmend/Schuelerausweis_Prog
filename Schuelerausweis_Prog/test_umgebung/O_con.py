#This file is for creating a connection to the Sqlite3 Database
#and executing a command
import sqlite3

#This is to change the name of the Database it will use
#'schuelerausweis.sqlite' as default

log = open('log\log_connection.txt', 'a')

#Zuerst wird eine Verbindung mit der Datenbank Hergestellt
    #Wenn keine verbindung möglich ist die Datenbank nicht vorhanden
        #oder der Datenbank Name Falsch
#Als Zweites wird der SQL befehl ausgeführt
    #Wenn der SQL Befehl nicht richtig ist wird ein error ausgeworfen



class Connect:
    def __init__(self):
        pass

    def con(command):
        sql_DB = "schuelerausweis.sqlite"
        log.write("Datenbank wird geöffnet.\n")
        try:
            connection = sqlite3.connect(sql_DB)
            cursor = connection.cursor()
            log.write("Datenbank verbindung Hergestellt.\n")
        except:
            log.write("Datenbank verbindung konnte nicht hergestellt werden.\n")
        try:
            sql = str(command)
            cursor.execute(sql)
            results = cursor.fetchall()
            log.write("SQL-Befehl: (" + command + ") Wurde erfolgreich ausgeführt.\n")
            return results
        except:
            log.write("SQL Befehl konnte nicht ausgeführt werden.\n")
        finally:
            cursor.close()
            log.write("Datenbank wurde erfolgreich geschlossen.\n")

Connect.con("SELECT * FROM schueler")
