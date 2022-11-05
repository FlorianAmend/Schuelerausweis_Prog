import csv
import sqlite3

sidfile = "sid_lusd.csv"
checkfile = "check.csv"
log  = open("log.txt", "a")

#Creating a Connection to the Database
connection = sqlite3.connect('schuelerausweis.db')
#Setting the I/O cummunication with the Database up
cursor = connection.cursor()

#Als erstes werden alle noch vorhanden schueler aus der Datenbank geholt
#Danach wird gecheckt welche schueler in der neuen LUSD.csv Datei vorhanden sind
#Wenn die schueler nicht mehr vorhanden sind in der lusd.csv aber in der Datenbank werden diese schueler gelöscht

def find_diff():
#    try:
    with open(sidfile, "r") as sid_file:
        lines_sid = sid_file.readlines()
        reader = csv.DictReader(sid_file)
        with open(checkfile, "r") as file:
            list_sid = []
            lines_check = file.readlines()
            read = csv.DictReader(file)
            x = set(lines_sid)
            y = set(lines_check)
            z = x.difference(y)
            z = z
            list_sid.append(z)
            for i in z:
                print(i)
                log.writelines("ist nicht in der sid_file.csv: " + str(i) + "\n")
                cursor.execute("DELETE FROM schueler WHERE sid=?", str((i,)))
                log.writelines("sid: " + str(i) + " wurde gelöscht.\n")
                file.close()
                sid_file.close()
#    except:
#        log.writelines("Schueler konnte nicht gelöscht werden.\n")

def get_all_sid():
    sql = "SELECT sid FROM schueler"
    cursor.execute(sql)
    result = cursor.fetchall()
    with open(sidfile, "w") as sid:
        writer = csv.writer(sid)
        writer.writerows(result)
    find_diff()

get_all_sid()

#connection.commit()
cursor.execute("SELECT * FROM schueler")
results = cursor.fetchall()
print(results)
cursor.close()
