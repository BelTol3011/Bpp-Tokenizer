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

# Einfache Operationen: "a=b+1", "a+=b", "a=a+1"
# [Var_Name,Operant'=',Var_Name,Operant='+',Integer] -> Zuweisung.Addition
# [Var_Name,Operant'=',Var_Name,Operant='-',Integer] -> Zuweisung.Subtraktion
# [Var_Name,Operant'=',Var_Name,Operant='/',Integer] -> Zuweisung.Division
# [Var_Name,Operant'=',Var_Name,Operant='*',Integer] -> Zuweisung.Multiplikation

# [Var_Name,Operant'+=',Var_Name]   -> Zuweisung.Addition
# [Var_Name,Operant'+=',Integer]    -> Zuweisung.Addition
# [Var_Name,Operant'*=',Var_Name]   -> Zuweisung.Multiplikation
# [Var_Name,Operant'*=',Integer]    -> Zuweisung.Multiplikation
# [Var_Name,Operant'/=',Var_Name]   -> Zuweisung.Division
# [Var_Name,Operant'/=',Integer]    -> Zuweisung.Division
# [Var_Name,Operant'-=',Var_Name]   -> Zuweisung.Subtraktion
# [Var_Name,Operant'-=',Integer]    -> Zuweisung.Subtraktion

# Einfache Operationen, Argumente vertauscht: "a=1+b"
# [Var_Name,Operant'=',Integer,Operant='+',Var_Name] -> Zuweisung.Addition
# [Var_Name,Operant'=',Integer,Operant='-',Var_Name] -> Zuweisung.Subtraktion
# [Var_Name,Operant'=',Integer,Operant='/',Var_Name] -> Zuweisung.Division
# [Var_Name,Operant'=',Integer,Operant='*',Var_Name] -> Zuweisung.Multiplikation





def tokenize(inputlist):
    for line in inputlist:
        for objekt in line:
            print(objekt.data, objekt.type)



    outputlist = inputlist


#Notiz: liste Tupels, nicht 2D: z.B: variable assignment, Variabelname,

    return outputlist
