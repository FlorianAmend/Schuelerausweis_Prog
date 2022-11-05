import csv
import base64
import sqlite3
import datetime
from configparser import ConfigParser
from dateutil.relativedelta import relativedelta
from datetime import date
from datetime import datetime
from random import randint, randrange
import O_GUI_prog as guip


#checkfile = "CSV\check.csv"

#Es fehlt eine nummer für die Bibliotheke und als sid
#Es fehlt die verarbeitung eines bildes

bid_num = []
bin_image = [None]


class AddPhoto:
    def __init__(self, path, vorname,nachname,gebdat):
        try:
            self.path = path
            self.vorname = vorname
            self.nachname = nachname
            self.gebdat = gebdat
            photo = SchuelerErstellen.convert_to_binary(self,path)
            sql_DB = "schuelerausweis.sqlite"
            connection = sqlite3.connect(sql_DB)
            cursor = connection.cursor()
            cursor.execute("UPDATE schueler SET foto=? WHERE vorname=? AND nachname=? AND gebdat=?", (photo,vorname,nachname,gebdat,))
            results = cursor.fetchall()
            print(results)
            connection.commit()
            cursor.close()
        except:
            with open("log/log_create_schueler.txt", "a") as logfile:
                logfile.write("Foto konnte nicht hinzugefügt werden\n")
                logfile.write("Error: (Class: AddPhoto)\n")
                logfile.close()

class SchuelerLoeschen:
    def __init__(self, vorname,nachname,gebdat):
        try:
            self.vorname = vorname
            self.nachname = nachname
            self.gebdat = gebdat
            connection = sqlite3.connect('schuelerausweis.sqlite')
            cursor = connection.cursor()
            cursor.execute("DELETE FROM schueler WHERE vorname=? AND nachname=? AND gebdat=? ", (vorname,nachname,gebdat,))
            connection.commit()
            cursor.close()
            log.write("Schueler wurde erfolgreich gelöscht")
        except:
            with open("log/log_create_schueler.txt", "a") as logfile:
                logfile.write("Fehler: Schueler nicht vorhanden")
                logfile.write("Error: (SchuelerLoeschen)\n")
                logfile.close()

class SchuelerErstellen:
    def __init__(self,status,kid,foto,nachname,vorname,gebdat):
        try:
            try:
                bid_num.pop()
            except:
                with open("log/log_create_schueler.txt", "a") as log:
                    log.write("Error: Keine BID im array vorhaden.\n")
                    log.close()
            with open("log/log_create_schueler.txt", "a") as log:
                self.nachname = nachname
                self.vorname = vorname
                self.status = status
                self.gebdat = gebdat
                self.foto = foto
                self.kid = kid
                print(bid_num)
                self.get_bid()
                self.del_line_bid()
                self.convert_to_binary(foto)
                sql_DB = "schuelerausweis.sqlite"
                connection = sqlite3.connect(sql_DB)
                cursor = connection.cursor()
                dig_to_Bin = bin_image[-1]
                bid = bid_num[-1]
                cursor.execute("SELECT * FROM klasse WHERE kid=?", (kid,))
                kid_result = cursor.fetchall()
                gueltig_bis = None
                lvorname = [vorname]
                lnachname = [nachname]
                avorname = lvorname[0].split()
                anachname = lnachname[0].split()
                awvorname = avorname[0]
                awnachname = anachname[-1]
                for k in kid_result:
                    ha = k[1]
                    tod = date.today()
                    calcHalb = ha // 2
                    calc = ha % 2
                    halbZeit = calc + calcHalb
                    if ((ha%2)==0):
                        gueltig_bis = date(year=tod.year+halbZeit,day=31,month=7)
                    else:
                        gueltig_bis = date(year=tod.year+halbZeit,day=1,month=1)
                einschu = date.today()
                sql = "SELECT vorname,nachname,gebdat FROM schueler WHERE vorname=? AND nachname=? AND gebdat=?"
                sql_insert = """INSERT INTO schueler (bid,status,kid,foto,auswname,nachname,auswvname,vorname,gebdat,einschulung,gültigbis) VALUES (?,?,?,?,?,?,?,?,?,?,?)"""
                datatulpe_sql = (vorname,nachname,gebdat)
                datatulpe =[bid,"Aktiv",kid,dig_to_Bin,awnachname,nachname,awvorname,vorname,gebdat,einschu,gueltig_bis]
                log.write("Schueler "+ str(datatulpe_sql) + " wird gesucht....\n")
                cursor.execute("SELECT bid,kid FROM schueler WHERE vorname=? AND nachname=? AND gebdat=?", (vorname,nachname,gebdat))
                results = cursor.fetchall()
                if(len(results)==0):
                    log.write("Schueler " + str(datatulpe_sql) + " wurde in der Datenbank nicht gefunden.\n")
                    log.write("Schueler " + str(datatulpe_sql) + " Wird in die Datenbank Hinzugefügt\n")
                    cursor.execute(sql_insert, datatulpe)
                    connection.commit()
                elif(len(results)!=0):
                    log.write("Schueler " + str(datatulpe) + " ist schon in der Datenbank vorhanden.\n")
                    for i in results:
                        klasse = i[1]
                        if (klasse!=kid):
                            cursor.execute("UPDATE schueler SET kid=? WHERE vorname=? AND nachname=? AND gebdat=?", (kid,vorname,nachname,gebdat,))
                            log.write("Klasse wurde geändert\n")
                            connection.commit()
                log.close()
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (Class: SchuelerErstellen(Import/Erstellen Part))\n")
                log.close()

    def get_bid(self):
        try:
            with open('numBid.txt', 'r') as bid:
                bid_unconv = bid.readlines(5)
                for element in bid_unconv:
                    bid_num.append(int(element.strip()))
                    print(bid_num)
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (get_bid)\n")
                log.close()

    def del_line_bid(self):
        try:
            lines = []
            with open('numBid.txt', 'r') as fp:
                lines = fp.readlines()
            with open('numBid.txt', 'w') as fp:
                for number, line in enumerate(lines):
                    if number not in [0]:
                        fp.write(line)
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (del_line_bid())\n")
                log.close()

    def convert_to_binary(self,filename):
        try:
            if (filename == None):
                #log.write("Es wurde kein Bild zur Datenbank hinzugefügt.\n")
                return None
            else:
                with open(filename, 'rb') as file:
                #    log.write("Es wurde ein Bild hinzugefügt.\n")
                    blobData = file.read()
                    bin_image.append(blobData)
                    return blobData
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (convert_to_binary())\n")
                log.close()

    def writeBinarytoFile(data, filename):
        try:
            with open(filename, 'wb') as file:
                file.write(data)
                return filename
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (writeBinarytoFile())\n")
                log.close()

class KlassenHinzufuegen:
    def __init__(self):
        self.ini()

    def ini(self):
        try:
            config = ConfigParser()
            config.optionxform = str
            config.read('config.ini')

            connection = sqlite3.connect('schuelerausweis.sqlite')
            cursor = connection.cursor()

            data = {}

            for section in config.sections():
                for key in dict(config.items(section)):
                    k = config['klasse']
                    data[key] = k.get(key)

            for klze in data.items():
                months = int(klze[1])
                years = months / 12
                days = years * 365
                cursor.execute("SELECT * FROM klasse WHERE kid=?", (klze[0],))
                results = cursor.fetchall()
                if (len(results)==0):
                    datatuple = (klze[0],months)
                    sql = "INSERT INTO klasse (kid,dauer) VALUES (?,?)"
                    cursor.execute(sql,datatuple)
                elif(len(results)!=0):
                    pass

            connection.commit()
            cursor.close()
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (Class: KlassenHinzufuegen)\n")
                log.close()

class SucheKlasse:
    def __init__(self):
        pass

    def suchen(name,kid):
        try:
            with open("log/log_create_schueler.txt", "a") as log:

                connection = sqlite3.connect('schuelerausweis.sqlite')
                cursor = connection.cursor()
                log.write("Klasse: (" + kid +") " "klasse(" + name + ") wird gesucht.\n")
                cursor.execute("SELECT vorname,nachname,gebdat,kid,gültigbis,foto,status FROM schueler WHERE kid=? AND nachname=? ", (kid,name,))
                results = cursor.fetchall()
                cursor.close()
                log.write("Klasse: (" + kid + ") wurde gefunden.\n")
                return results
                log.close()
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (SucheKlasse.suche())\n")
                log.write("Klasse und name: (" + kid + name + ") wurde nicht gefunden.\n")
                log.close()

    def suche_name(name):
        try:
            with open("log/log_create_schueler.txt", "a") as log:

                connection = sqlite3.connect('schuelerausweis.sqlite')
                cursor = connection.cursor()
                log.write("Nachname: (" + name + ") wird gesucht.\n")
                cursor.execute("SELECT vorname,nachname,gebdat,kid,gültigbis,foto,status FROM schueler WHERE nachname=?", (name,))
                results = cursor.fetchall()
                print(results)
                cursor.close()
                log.write("Name: (" + name + ") wurde gefunden.\n")
                return results
                log.close()
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (SucheKlasse.suche_name)\n")
                log.write("Name: (" + name + ") wurde nicht gefunden.\n")
                log.close()

    def suche_klasse(kid):

        try:
            with open("log/log_create_schueler.txt", "a") as log:

                connection = sqlite3.connect('schuelerausweis.sqlite')
                cursor = connection.cursor()
                log.write("Klasse: (" + kid + ") wird gesucht.\n")
                cursor.execute("SELECT vorname,nachname,gebdat,kid,gültigbis,foto,status FROM schueler WHERE kid=? ORDER BY nachname ASC", (kid,))
                results = cursor.fetchall()
                cursor.close()
                log.write("Name: (" + kid + ") wurde gefunden.\n")
                return results
                log.close()
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Error: (SucheKlasse.suche_klasse)\n")
                log.write("Name: (" + kid + ") wurde nicht gefunden.\n")
                log.close()

class SchuelerBildDel:
    def __init__(self, vorname,nachname,gebdat):
        try:
            with open("log/log_create_schueler.txt", "a") as log:
                self.vorname = vorname
                self.nachname = nachname
                self.gebdat = gebdat
                foto =None
                connection = sqlite3.connect('schuelerausweis.sqlite')
                cursor = connection.cursor()
                cursor.execute("UPDATE schueler SET foto = null WHERE vorname = ? AND nachname = ? AND gebdat = ?", (vorname,nachname,gebdat,))
                connection.commit()
                cursor.close()
                log.write("Schueler Bild wurde erfolgreich gelöscht")
                log.close()
        except:
            with open("log/log_create_schueler.txt", "a") as log:
                log.write("Fehler: Schueler nicht vorhanden")
                log.write("Error: (SchuelerLoeschen)\n")
                log.close()
