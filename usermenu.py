import db_mod

while True:                                                                                                                                             #Endlosschleife -> Programm muss mit Exit verlassen werden
    aktion = input("\n (1) Datenbanken auflisten \n (2) Tabellen einer DB auflisten \n (3) Datenbank erstellen \n (4) Gerät hinzufügen \n (5) Statistik eines Geräts ausgeben \n (6) Exit\n\n")      

    if aktion == "1":                                                                                                                                   #Aktion 1: Alle Datenbanken werden aufgelistet
        print("\n")
        db_mod.listdb()
        
    elif aktion == "2":                                                                                                                                 #Aktion 2: Listet alle Tabellen/Geräte in einer Datenbank auf
        dbname = input("\nAuf welche Datenbank möchtest du zugreifen? Eine Liste der verfügbaren Datenbanken kannst du im Hauptmenü aufrufen!\n")
        try:                                                                                                                            
            cur_db = db_mod.connect(dbname)                                                                                                             #Hier wird geprüft ob die DB existiert, dafür muss Verbindung geschaffen werden
        except:
            print("\nDiese Datenbank existiert nicht! Du kannst sie aber in Punkt 3 im Hauptmenü erstellen!\n")                                         #Auflistung erfolgt nur wenn DB existent
            continue
        print("\nVerfügbare Geräte in " + dbname + ":\n")
        db_mod.listtable(cur_db)                                                                                                                        #Hier geschieht die Auflistung
        db_mod.disconnect(cur_db)                                                                                                                       #Verbindung zur DB gekappt, da nicht mehr benötigt

    elif aktion == "3":                                                                                                                                 #Aktion 3: Datenbank wird erstellt, falls sie nicht existiert
        dbname = input("\nWie soll deine Datenbank heißen?\n")
        db_mod.checkdb(dbname)

    elif aktion == "4":                                                                                                                                 #Aktion 4: Fügt Gerät hinzu, indem es eine entsprechende gleichnamige Tabelle anlegt
        dbname = input("\nAuf welche Datenbank möchtest du zugreifen? Eine Liste der verfügbaren Datenbanken kannst du im Hauptmenü aufrufen!\n")       #Auch hier wird Existenz der DB geprüft
        try:                                                                                                                            
            cur_db = db_mod.connect(dbname)
        except:
            print("\nDiese Datenbank existiert nicht! Du kannst sie aber in Punkt 3 im Hauptmenü erstellen!\n")
            continue
        tablename = input("\nWie soll das Gerät heißen?\n")
        if db_mod.checktable(cur_db,tablename) != True:                                                                                                 #Erstellung der Tabelle/Hinzufügen des Geräts nur wenn nicht schon eine Tabelle mit gleichem Namen existiert
            db_mod.add_device(cur_db,tablename)
            print("Falls noch nicht geschehen, solltest du das Programm 'cpumonitoring.py' auf deinem neuen Gerät starten, sowie die DB- und den Gerätenamen einstellen.")
            print("Nur so werden die Daten des Geräts aufgezeichnet und es kann eine Statistik erstellt werden.")
        else:
            print("\nDas Gerät wurde bereits hinzugefügt!\n")
            continue
        db_mod.disconnect(cur_db)                                               

    elif aktion == "5":                                                                                                                                 #Aktion 5: Statistik eines Geräts einer Datenbank wird ausgegeben
        dbname = input("\nAuf welche Datenbank möchtest du zugreifen? Eine Liste der verfügbaren Datenbanken kannst du im Hauptmenü aufrufen!\n")
        try:                                                                                                                                            #try-except falls eingegebene DB nicht existiert
            cur_db = db_mod.connect(dbname)
        except:
            print("\nDiese Datenbank existiert nicht! Du kannst sie aber in Punkt 3 im Hauptmenü erstellen!\n")
            continue                                                                                                                                    #continue springt zum Anfang Hauptmenü (Neue Iteration der Endlos-Schleife)

        table = input("\nWelches Gerät möchtest du auswählen? Eine Liste der verfügbaren Geräte kannst du im Hauptmenü aufrufen!\n")
        if db_mod.checktable(cur_db,table) != True:                                                                                                     #Die Statistikerstellung läuft nur weiter wenn Gerät/Tabelle auch existiert
            print("\nDieses Gerät existiert nicht! Du kannst es aber in Punkt 4 im Hauptmenü erstellen!\n")
            continue
            
        print("\nNun gib an, über welchen Zeitraum Daten für die Statistik verwendet werden sollen.")                                                   #Option den Zeitraum der Statistik selbst zu bestimmen, anstatt immer nur 2 Stunden
        dig = input("Gibt zuerst die Zahl und gleich die Zeiteinheit an. \n")
        unit = input("Gibt nun die Zeiteinheit an: \n (1) Minuten \n (2) Stunden \n (3) Tage \n")                                                       #Auswahlmenü um User-Fehler zu vermeiden

        if unit == "1":
            interval = dig + " MINUTE"

        elif unit == "2":
            interval = dig + " HOUR"

        elif unit == "3":
            interval = dig + " DAY"

        else:
            print("\nWähle eine der oben stehenden Optionen aus!\n")                                                                                    #Auch hier nur bestehende Auswahl wählen
            continue
                
        db_mod.stats(cur_db,table,interval)                                                                                                             #Funktion Stats in Modul wird ausgeführt mit gewählter DB, Gerät(Tabelle) und Zeitintervall als Parameter
        db_mod.disconnect(cur_db)                                                                                                                       #Funktion disconnect unterbricht die Verbindung zur gewählten Datenbank

    elif aktion == "6":                                                                                                                                 #Exit-Aktion aus dem Benutzermenü
        break;

    else:
        print("\nWähle eine der 6 Optionen aus!")                                                                                                       #Es soll nur aus den Optionen im Menü gewählt werden
        continue
        
