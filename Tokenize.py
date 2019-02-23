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
# [Comment] -> Kommentar
# [Var_Name,Operant'=',Integer]  -> Zuweisung.Integer
# [Var_Name,Operant'=',Var_Name] -> Zuweisung.Variable
# [Var_Name,Space,Operant'=',Space,Integer]  -> Zuweisung.Integer
# [Var_Name,Space,Operant'=',Space,Var_Name] -> Zuweisung.Variable

# Einfache Operationen "a+=1", "a+=b"
# [Var_Name,Operant'+=',Var_Name]   -> Zuweisung.Addition
# [Var_Name,Operant'+=',Integer]    -> Zuweisung.Addition
# [Var_Name,Operant'*=',Var_Name]   -> Zuweisung.Multiplikation
# [Var_Name,Operant'*=',Integer]    -> Zuweisung.Multiplikation
# [Var_Name,Operant'/=',Var_Name]   -> Zuweisung.Division
# [Var_Name,Operant'/=',Integer]    -> Zuweisung.Division
# [Var_Name,Operant'-=',Var_Name]   -> Zuweisung.Subtraktion
# [Var_Name,Operant'-=',Integer]    -> Zuweisung.Subtraktion
# Einfache Operationen, mit Space: "a += 1", "a += b"
# [Var_Name,Space,Operant'+=',Space,Var_Name]   -> Zuweisung.Addition
# [Var_Name,Space,Operant'+=',Space,Integer]    -> Zuweisung.Addition
# [Var_Name,Space,Operant'*=',Space,Var_Name]   -> Zuweisung.Multiplikation
# [Var_Name,Space,Operant'*=',Space,Integer]    -> Zuweisung.Multiplikation
# [Var_Name,Space,Operant'/=',Space,Var_Name]   -> Zuweisung.Division
# [Var_Name,Space,Operant'/=',Space,Integer]    -> Zuweisung.Division
# [Var_Name,Space,Operant'-=',Space,Var_Name]   -> Zuweisung.Subtraktion
# [Var_Name,Space,Operant'-=',Space,Integer]    -> Zuweisung.Subtraktion

# Einfache Operationen: "a=b+1", "a= a/b", "a=a*1"
# [Var_Name,Operant'=',Var_Name,Operant='+',Integer] -> Zuweisung.Addition
# [Var_Name,Operant'=',Var_Name,Operant='-',Integer] -> Zuweisung.Subtraktion
# [Var_Name,Operant'=',Var_Name,Operant='/',Integer] -> Zuweisung.Division
# [Var_Name,Operant'=',Var_Name,Operant='*',Integer] -> Zuweisung.Multiplikation
# Einfache Operationen, mit Space: "a = a + 1"
# [Var_Name,Space,Operant'=',Space,Var_Name,Operant='+',Space, Integer] -> Zuweisung.Addition
# [Var_Name,Space,Operant'=',Space,Var_Name,Operant='-',Space, Integer] -> Zuweisung.Subtraktion
# [Var_Name,Space,Operant'=',Space,Var_Name,Operant='/',Space, Integer] -> Zuweisung.Division
# [Var_Name,Space,Operant'=',Space,Var_Name,Operant='*',Space, Integer] -> Zuweisung.Multiplikation

# Einfache Operationen, Argumente vertauscht: "a=1+b"
# [Var_Name,Operant'=',Integer,Operant='+',Var_Name] -> Zuweisung.Addition
# [Var_Name,Operant'=',Integer,Operant='-',Var_Name] -> Zuweisung.Subtraktion
# [Var_Name,Operant'=',Integer,Operant='/',Var_Name] -> Zuweisung.Division
# [Var_Name,Operant'=',Integer,Operant='*',Var_Name] -> Zuweisung.Multiplikation
# Einfache Operationen, Argumente vertauscht: "a = 1 + b"
# [Var_Name,Space,Operant'=',Space,Integer,Space,Operant='+',Space,Var_Name] -> Zuweisung.Addition
# [Var_Name,Space,Operant'=',Space,Integer,Space,Operant='-',Space,Var_Name] -> Zuweisung.Subtraktion
# [Var_Name,Space,Operant'=',Space,Integer,Space,Operant='/',Space,Var_Name] -> Zuweisung.Division
# [Var_Name,Space,Operant'=',Space,Integer,Space,Operant='*',Space,Var_Name] -> Zuweisung.Multiplikation


# tbd: ist "Name" ein "Var_Name" oder "Fun_Name"

#if schleifen
#
ObjectChain = [
[Parser.Comment], #-> Kommentar
[Var_Name,Operant'=',Integer],  #-> Zuweisung.Integer
[Var_Name,Operant'=',Var_Name], #-> Zuweisung.Variable
[Var_Name,Space,Operant'=',Space,Integer],  #-> Zuweisung.Integer
[Var_Name,Space,Operant'=',Space,Var_Name], #-> Zuweisung.Variable


]

def tokenize(inputlist):
    for line in inputlist:
        for objekt in line:
            print(objekt.data, objekt.type)
        print("newlne")


    #debug
    outputlist = inputlist


#Notiz: liste Tupels, nicht 2D: z.B: variable assignment, Variabelname,

    return outputlist
