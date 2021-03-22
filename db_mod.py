import mysql.connector                                                                                                          #Import nötig für MySQL in Python

def connect(dbname):                                                                                                            #connect-Funktion stellt Verbindung zur übergebenen DB her
    mydb = mysql.connector.connect(
	host = "localhost",                                                                                                     #Standard-Einlogdaten für DB
	user = "root",
	password = "",
	database= dbname
    )
    return mydb                                                                                                                 #Rückgabewert ist die Schnittstelle zur DB
    mydb.close()                                                                                                                #Da schon als Kopie an Hauptprogramm zurückgegeben, kann diese Instanz geschlossen werden 


def disconnect(db):
    db.close()                                                                                                                  #Kappt Verbindung zur DB

def send(table,time,cpu,ram,db):                                                                                                #Sendet übergebene Daten an spezifizierte DB und Tabelle
    mycursor = db.cursor()                                                                                                      #Der auf die angegebene DB gerichtete Cursor führt SQL Aktionen an DB aus
    mycursor.execute("INSERT INTO %s (Timestamp,CPU,RAM) VALUES('%s', '%s', '%s');"% (table,time,cpu,ram))                      #Timestamp,CPU und RAM Daten werden in genannte Tabelle eingetragen
    db.commit()                                                                                                                 #commit für tatsächliche Anpassung in Tabelle
    mycursor.close()                                                                                                            #Cursor kann geschlossen werden

    
def stats(db,table,interval):                                                                                                   #stats-Funktion liest Daten aus gegebener DB/Tabelle aus und erstellt eine Statistik, welche Daten aus einem angegebenen Zeitintervall nutzt
    print("\n","MIN_CPU \t MAX_CPU \t AVG_CPU \t MIN_RAM \t MAX_RAM \t AVG_RAM")                                                #Überschrift
    mycursor = db.cursor()                                                                                                      #Cursor wird wieder auf angegebene DB gerichtet

    mycursor.execute("SELECT MIN(CPU) FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL %s);"% (table,interval))              #Der kleinste CPU-Wert in der übergebenen Tabelle mit Zeitsempel größer gleich die aktuelle Zeit minus ein ausgewähltes Zeitintervall wird ausgelesen 
    min_cpu = mycursor.fetchone()[0]                                                                                            #Der Wert wird in Variable gspeichert

    mycursor.execute("SELECT MAX(CPU) FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL %s);"% (table,interval))              #das gleiche mit max CPU Wert
    max_cpu = mycursor.fetchone()[0]

    mycursor.execute("SELECT AVG(CPU) FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL %s);"% (table,interval))              #das gleiche mit durchschnittlichem CPU Wert
    avg_cpu = mycursor.fetchone()[0]

    mycursor.execute("SELECT MIN(RAM) FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL %s);"% (table,interval))              #ab hier mit RAM
    min_ram = mycursor.fetchone()[0]

    mycursor.execute("SELECT MAX(RAM) FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL %s);"% (table,interval))
    max_ram = mycursor.fetchone()[0]

    mycursor.execute("SELECT AVG(RAM) FROM %s WHERE Timestamp >= DATE_SUB(NOW(), INTERVAL %s);"% (table,interval))
    avg_ram = mycursor.fetchone()[0]

    try:
        print("",min_cpu,"\t\t",max_cpu,"\t\t",round(avg_cpu,2) ,"\t\t",min_ram,"\t\t",max_ram,"\t\t",round(avg_ram,2),"\n")    #Ausgabe der Werte unter der Überschrift mit gerundeten Durchschnittswerten
    except:
        print("",min_cpu,"\t\t",max_cpu,"\t\t",avg_cpu ,"\t\t",min_ram,"\t\t",max_ram,"\t\t",avg_ram,"\n")                      #try-excep nötig ohne Rundungen falls im angegebenen Zeitraum keine Werte stehen, da round Funktion sonst Fehler ausgibt
    
    mycursor.close()

def checkdb(dbname):                                                                                                            #Funktion checkdb prüft ob DB vorhanden -> falls nicht wird sie erstellt
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database= dbname                                                                                                    #wenn diese Zeile keinen Fehler generiert, exisitiert die DB
        )
        print("\n\nDatenbank '" + dbname + "' existiert bereits!\n")
    except:
        mydb = mysql.connector.connect(                                                                                         #Except Teil wird ausgelöst wenn Fehler generiert wurde
            host = "localhost",
            user = "root",
            password = "",
        )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE %s;"% (dbname))                                                                       #Datenbank mit gewähltem Namen wird erstellt
        mycursor.close()
        print("\n\nDatenbank '" + dbname + "' wurde erstellt.\n")
        mydb.close()

def listdb():                                                                                                                   #Funktion listet Datenbanken auf
    mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = ""
    )
    mycursor = mydb.cursor()

    mycursor.execute("SHOW DATABASES")

    for x in mycursor:
        print(x)
        
    mycursor.close()
    mydb.close()

def checktable(db,table):                                                                                                       #Funktion prüft ob Tabelle vorhanden ist
    mycursor = db.cursor()

    mycursor.execute("SHOW TABLES LIKE '%s'"% (table))                                                                          #listet Tabellennamen auf, die wie der übergebene Name sind

    for x in mycursor:                                      
        if table in x:                                                                                                          #Tabellennamen muss nur in x vorkommen, da mit "SHOW TABLES" Tabellennamen so ausgelesen werden : "(tabellenname);". Fehler dadurch können nicht vorkommen, da mir "SHOW TABLES LIKE ..." schon gefiltert wurde
            return True
        else:
            return False

def add_device(db,tablename):                                                                                                   #Erstellt neue Tabelle                           
    mycursor = db.cursor()

    mycursor.execute("CREATE TABLE %s (Timestamp TIMESTAMP, CPU FLOAT, RAM FLOAT);"% (tablename))                               #Erstellt Tabelle mit gewähltem Namen mit Timestamp, CPU und RAM Spalte
    print("\nGerät '" + tablename + "' wurde erstellt.\n")
    mycursor.close()

def listtable(db):                                                                                                              #Funktion listet alle Tabellen einer spezifizierten DB auf
    mycursor = db.cursor()

    mycursor.execute("SHOW TABLES")

    for x in mycursor:                                      
        print(x)
        
    mycursor.close()
