import csv
import base64
import sqlite3
import datetime
from dateutil.relativedelta import relativedelta
from random import randint, randrange

csvfile = "lusd_2.csv"
checkfile = "check.csv"
log = open("log.txt", "a")
#bid_read = open("bid_check.txt", "r")
#bid_write = open("bid_check.txt", "a")
#Creating a Connection to the Database
connection = sqlite3.connect('schuelerausweis.db')
#Setting the I/O cummunication with the Database up
cursor = connection.cursor()

def creat_bid():
    count = 184752317
    for i in range(count,999999999):
            bid_write.write(str(i) + "\n")
            count += 1
            if (count == 100000):
                break

def del_bid():
    a_file = open("sample.txt", "r")
    lines = a_file.readlines()
    a_file.close()
    del lines[0]
    new_file = open("sample.txt", "w+")
    for line in lines:
        new_file.write(line)
    new_file.close()

def base64_decode(liste):
    base64_message = str(liste)
    base64_bytes = base64_message.encode('ascii')
    message_bytes_de =  base64.b64decode(base64_bytes)
    message = message_bytes_de.decode('ascii')
    return message

def base64_convert(liste):
    message = str(liste)
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

def create_sid_check():
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



def find_DB():
    with open(csvfile) as file:
        reader = csv.DictReader(file)
        for row in reader:
            datatulpe = (row['Schueler_Vorname'],row['Schueler_Nachname'],row['Klassen_Klassenbezeichnung'],row['Schueler_Geburtsdatum'])
            e = base64_convert(datatulpe)
            log.write("Schueler "+ str(datatulpe) + " wird gesucht....\n")
            cursor.execute("SELECT sid FROM schueler WHERE sid=?", (e,))
            results = cursor.fetchall()
            if(len(results)==0):
                log.write("Schueler " + str(datatulpe) + " wurde in der Datenbank nicht gefunden.\n")
                log.write("Schueler " + str(datatulpe) + " Wird in die Datenbank Hinzugefügt\n")
                erstell_schuler_csv("aktiv",row['Klassen_Klassenbezeichnung'],None,row['Schueler_Nachname'],row['Schueler_Vorname'],row['Schueler_Geburtsdatum'])
            else:
                log.write("Schueler " + str(datatulpe) + " ist schon in der Datenbank vorhanden.\n")
    file.close()

def convert_to_binary(filename):
    if (filename == None):
        return None
    else:
        with open(filename, 'rb') as file:
            blobData = file.read()
            return blobData

#def erstell_einz_schueler(status,nachname,vorname,gebdat):

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
    finally:
        create_sid_check()

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

suche_klasse('11BFI5')

#create_sid_check()
#find_DB()

#connection.commit()
#cursor.execute("SELECT * FROM schueler")
#results = cursor.fetchall()
#print(results)
cursor.close()



            #####ENCODE
            #message_bytes = i.encode('ascii')
            #base64_bytes = base64.b64encode(message_bytes)
            #encoded schueler id
            #base64_message = base64_bytes.decode('ascii')

            #####DECODE
#            base64_de = base64_message.encode('ascii')
#            message_bytes_de =  base64.b64decode(base64_bytes)
#            message = message_bytes_de.decode('ascii')
#            print(message)
