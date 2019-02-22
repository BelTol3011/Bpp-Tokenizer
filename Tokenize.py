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
# [Comment] -> Kommentar
# a+=b


# Einfache Operationen: "a=b+1"
# [Var_Name1,Operant'=',Var_Name2,Operant='+',Integer] -> Zuweisung.Addition
# [Var_Name1,Operant'=',Var_Name2,Operant='-',Integer] -> Zuweisung.Subtraktion
# [Var_Name1,Operant'=',Var_Name2,Operant='/',Integer] -> Zuweisung.Division
# [Var_Name1,Operant'=',Var_Name2,Operant='*',Integer] -> Zuweisung.Multiplikation

# [Var_Name1,Operant'+=',Var_Name2] -> Zuweisung.Addition
# [Var_Name1,Operant'+=',Integer]   -> Zuweisung.Addition


# Einfache Operationen, Argumente vertauscht: "a=1+b"
# [Var_Name1,Operant'=',Integer,Operant='+',Var_Name2] -> Zuweisung.Addition
# [Var_Name1,Operant'=',Integer,Operant='-',Var_Name2] -> Zuweisung.Subtraktion
# [Var_Name1,Operant'=',Integer,Operant='/',Var_Name2] -> Zuweisung.Division
# [Var_Name1,Operant'=',Integer,Operant='*',Var_Name2] -> Zuweisung.Multiplikation





def tokenize(inputlist):
    for line in inputlist:
        for objekt in line:
            print(objekt.data, objekt.type)



    outputlist = inputlist


#Notiz: liste Tupels, nicht 2D: z.B: variable assignment, Variabelname,

    return outputlist
