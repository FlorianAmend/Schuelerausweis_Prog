import csv
import base64
import sqlite3
import O_con
import datetime
from dateutil.relativedelta import relativedelta
from random import randint, randrange


csvfile = "CSV\LUSD_testDaten.csv"
checkfile = "CSV\check.csv"
log = open("log\log_create_schueler.txt", "a")


class Schueler_erstellen:
    def __init__(self,status,kid,foto,nachname,vorname,gebdat):
        self.status = status
        self.kid = kid
        self.foto = foto
        self.nachname = nachname
        self.vorname = vorname
        self.gebdat = gebdat

    def erstell_schuler_csv(status,kid,foto,nachname,vorname,gebdat):
        try:
            #bid = creat_bid()
            dig_to_Bin = convert_to_binary(foto)
            one_for_all =  vorname,nachname,kid,gebdat
            datalist =  one_for_all
            base64_con = base64_convert(datalist)
            einschu = datetime.datetime.now()
            gueltig_bis = einschu + relativedelta(years=2)
            bid = None
            datatulpe =(base64_con,bid,status, kid, dig_to_Bin, nachname, vorname, gebdat,einschu,gueltig_bis)
            sql_insert = """INSERT INTO schueler (sid,bid,status,kid,foto,nachname,vorname,gebdat,einschulung,gültigbis) VALUES (?,?,?,?,?,?,?,?,?,?)"""
            cursor.execute(sql_insert, datatulpe)
            log.write("Schueler " + str(one_for_all) + " wurde erfolgreich zur Datenbank hinzugefügt.\n")
        except:
            log.write("Etwas ist beim erstellen des Schuelers " + str(one_for_all) + " Falsch gelaufen.\n")
        #finally:
            #create_sid_check()





class Not_now:
    def __init__(self):
        pass




    def creat_bid(self):
        count = 184752317
        for i in range(count,999999999):
                bid_write.write(str(i) + "\n")
                count += 1
                if (count == 100000):
                    break

    def del_bid(self):
        a_file = open("sample.txt", "r")
        lines = a_file.readlines()
        a_file.close()
        del lines[0]
        new_file = open("sample.txt", "w+")
        for line in lines:
            new_file.write(line)
        new_file.close()

#Methode base64_decode Decodes einen gegeben base64 String
#in den normalen String wieder

    def base64_decode(self,liste):
        base64_message = str(liste)
        base64_bytes = base64_message.encode('ascii')
        message_bytes_de =  base64.b64decode(base64_bytes)
        message = message_bytes_de.decode('ascii')
        return message

#Methode base64_convert Encodes eine gegeben liste in base64
#und gibt diese als String zurück
    def base64_convert(self,liste):
        message = str(liste)
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        return base64_message


#Methode 'create_sid_check' erstellt für jeden schueler in der CSV Datei
#in einen base64 String und fügt diesen String in die Check.csv
#welches dann für den zukünftigen cleanup benutzt wird

    def create_sid_check(self):
        sid_list = []
        with open(csvfile, "r") as lusd:
            reader = csv.DictReader(lusd)
            with open(checkfile, "w") as check:
                writer = csv.writer(check)
                for row in reader:
                    datatulpe = (row['Schueler_Vorname'],row['Schueler_Nachname'],row['Klassen_Klassenbezeichnung'],row['Schueler_Geburtsdatum'])
                    e = base64_convert(datatulpe)
                    sid_list.append(e)
                    writer.writerow((e,))



#Bei dieser Methode wird geschaut ob der Schueler schon in der Datenbank vorhanden ist
#Als erstes wird eine SID erstellt mit base64
#Danach wird der Schueler in der Datenbank gesucht
    #ist die SID schon vorhanden
        #wird der schueler nicht neu erstellt
    #ist die SID nicht vorhanden wird ein schueler erstellt


    def find_DB(self):

        with open(csvfile) as file:
            reader = csv.DictReader(file)
            for row in reader:
                datatulpe = (row['Schueler_Vorname'],row['Schueler_Nachname'],row['Klassen_Klassenbezeichnung'],row['Schueler_Geburtsdatum'])
                e = base64_convert(datatulpe)
                log.write("Schueler "+ str(datatulpe) + " wird gesucht....\n")
                O_con.Connect.con("SELECT sid FROM schueler WHERE sid=%s" % e)
                results = cursor.fetchall()
                if(len(results)==0):
                    log.write("Schueler " + str(datatulpe) + " wurde in der Datenbank nicht gefunden.\n")
                    log.write("Schueler " + str(datatulpe) + " Wird in die Datenbank Hinzugefügt\n")
                    erstell_schuler_csv("aktiv",row['Klassen_Klassenbezeichnung'],None,row['Schueler_Nachname'],row['Schueler_Vorname'],row['Schueler_Geburtsdatum'])
                else:
                    log.write("Schueler " + str(datatulpe) + " ist schon in der Datenbank vorhanden.\n")
        file.close()

#Die Methode 'convert_to_binary' wandelt gegeben Bilder in Binary form um
#Wenn kein Bild jedoch gegeben ist
    #Wird 'None' zurück gegeben

    def convert_to_binary(self,filename):
        if (filename == None):
            log.write("Es wurde kein Bild zur Datenbank hinzugefügt.\n")
            return None
        else:
            with open(filename, 'rb') as file:
                log.write("Es wurde ein Bild hinzugefügt.\n")
                blobData = file.read()
                return blobData



    def suche_klasse(kid):
        connection = sqlite3.connect('schuelerausweis.db')
        cursor = connection.cursor()
        log.write("Klasse: (" + kid + ") wird gesucht.\n")
        cursor.execute("SELECT vorname,nachname,gebdat FROM schueler WHERE kid=?", (kid,))
        try:
            results = cursor.fetchall()
            print(results[0])
            connection.commit()
            cursor.close()
            log.write("Klasse: (" + kid + ") wurde gefunden.\n")
            return results
        except:
            log.write("Error Code: 50")
            log.write("Klasse: (" + kid + ") wurde nicht gefunden.\n")
