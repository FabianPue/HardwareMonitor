"""
    Programm zum Auslesen der CPU- und RAM-
    Auslastung und Export in das CSV-Datenformat.

    Autor:  K. Faengmer
    Datum:  09.12.2020
"""


import psutil
import db_mod
from datetime import datetime

while True:                                                                                 #Endlosschleife für DB und Tabellen-/Gerätewahl
    dbname = input("\nIn welcher Datenbank sollen die Daten gespeichert werden?\n") 
    try:                                                                                    #try-except falls eingegebene DB nicht existiert
        cur_db = db_mod.connect(dbname)                                                     #Verbindung zur DB wird aufgenaut, falls sie existiert
        print("\nDatenbank '" + dbname + "' ausgewählt!")
    except:
        print("\nDiese Datenbank existiert nicht!\n")
        continue

    table = input("\nIn welcher Tabelle sollen die Daten gespeichert werden?\n")
    if db_mod.checktable(cur_db,table) == True:
        print("\nGerät '" + table + "' ausgewählt!\n")
        break                                                                               #Wenn Tabelle/Gerät existiert, wird Schleife durchbrochen und Hauptprogramm startet
    else:
        print("Diese Tabelle existiert nicht!")                                             #sonst wieder zurück auf Anfang
        continue
                                            

print("Timestamp \t\t CPU \t\t RAM")                                                        #Hier zusätzlich Überschriften eingefügt    
try:
    while True:            
        #Zeit und Auslastung ermitteln
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cpu = psutil.cpu_percent(1)
        ram = psutil.virtual_memory().percent
    
        db_mod.send(table,time,cpu,ram,cur_db)                                              #send-Funktion in db_mod sendet Daten an gewählte Datenbank in gewählte Tabele
        
        #Bildschirmausgabe
        print(time,"\t",cpu,"\t\t",ram)
            
except KeyboardInterrupt:
    print("... Abbruch!")

db_mod.disconnect(cur_db)                                                                   #Zum Schluss wird Verbindung zur Datenbank unterbrochen mit disconnect-Funktion
