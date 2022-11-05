#This file is to clean the Database of data that is not needed
#anymore. Such as Students that graduated or Students that left the school

#Importing CSV library and O_con library
#(O_con library is for the connection to the database
#which can be handelt like this 'Connect(#)')


#Als erstes werden alle -sid aus der Datenbank geholt
#Danach werden alle sid von der DB in die 'sidfile' geschrieben



import csv
import sqlite3
import O_con


sidfile = "CSV\sid_lusd.csv"
checkfile = "CSV\check.csv"
log = open('log\log_clean.txt', 'a')

#O_con.Connect("SELECT * FROM schueler")


class Cleanup:
    def __init__(self):
        self.get_all_sid()
        self.find_diff()


    def find_diff(self):
        print("donehere")
        with open(sidfile, "r") as sid_file:
            lines_sid = sid_file.readlines()
            reader = csv.DictReader(sid_file)
            with open(checkfile, "r") as file:
                list_sid = []
                print('done herer twoo')
                lines_check = file.readlines()
                read = csv.DictReader(file)
                x = set(lines_sid)
                y = set(lines_check)
                z = x.difference(y)
                z = z
                list_sid.append(z)
                for i in z:
                    print(i)
                    log.write("ist nicht in der sid_file.csv: " + "(" + str(i))
                    #schueler kann nicht gelöscht werden
                    O_con.Connect.con("DELETE FROM schueler WHERE sid = '%s'333*" % i)
                    log.write("wurde gelöscht.\n")
                    file.close()
                    sid_file.close()




    def get_all_sid(self):
        sql = "SELECT sid FROM schueler"
        result = O_con.Connect.con(sql)
        with open(sidfile, "w") as sid:
            writer = csv.writer(sid)
            writer.writerows(result)

Cleanup()
