import sys
import dump
import Parser

arguments = sys.argv

# Strg+Alt+L : Reformat
#
#
# Aufgaben:
# bekommt eine 2D-Liste, geschachtelt mit Tupels
# In Tokens umwandeln:
# Die Objekttypen sind vom parser übergeben worden
# die tokenize funktion beschreibt durch logische KOmbination der Tupels die Sprachkonstrukte
# Zuletzt die Liste mit dump in eine datei speichern


# Objektfolgen:
# [Var_Name,Operant'=',Integer]  -> Zuweisung
# [

def tokenize(inputlist):
    for line in inputlist:
        for objekt in line:
            print(objekt.data, objekt.type)



    outputlist = inputlist


#Notiz: liste Tupels, nicht 2D: z.B: variable assignment, Variabelname,

    return outputlist
