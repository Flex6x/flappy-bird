# datei_aenderer.py
import random
import re

def bird_aendern(dateiname, muster, neue_zeile):
    with open(dateiname, 'r') as datei:
        inhalt = datei.read()

    inhalt = re.sub(muster, neue_zeile, inhalt)

    with open(dateiname, 'w') as datei:
        datei.write(inhalt)

def schwierigkeit_aendern(dateiname, muster, neue_zeile):
    with open(dateiname, 'r') as datei:
        inhalt = datei.read()

    inhalt = re.sub(muster, neue_zeile, inhalt)

    with open(dateiname, 'w') as datei:
        datei.write(inhalt)

if __name__ == "__main__":
    dateiname = "flappy_bird.py" 
    muster = r"vogel\d*\.png"  
    v = input("Bird wählen: Main Bird [1] / Yellow Bird [2] / Red Bird [3] / Blue Bird [4]")
    if v == "1":
        neue_nummer = 1
    elif v == "2":
        neue_nummer = 2
    elif v == "3":
        neue_nummer = 3
    elif v == "4":
        neue_nummer = 4
    else:
        print ("Falsche Eingabe")
    neue_zeile = f"vogel{neue_nummer}.png"
    bird_aendern(dateiname, muster, neue_zeile)
    print(f"Der Vogel wurde erfolgreich geändert.")


if __name__ == "__main__":
    dateiname = "flappy_bird.py"  
    muster = r"self.rect.x -= 5"  
    va = input("Bird wählen: normal [1] / schnell [2] / sehr schnell [3]")
    if va == "1":
        neue_nummer = 5
    elif va == "2":
        neue_nummer = 10
    elif va == "3":
        neue_nummer = 15
    
    else:
        print ("Falsche Eingabe")
    neue_zeile = f"self.rect.x -={neue_nummer}"
    bird_aendern(dateiname, muster, neue_zeile)
    print(f"Der Vogel wurde erfolgreich geändert.")