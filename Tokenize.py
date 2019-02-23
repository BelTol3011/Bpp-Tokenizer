import sys
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
# [Name,Operant'=',Integer]  -> Zuweisung.Integer
# [Name,Operant'=',Name] -> Zuweisung.Variable
# [Name,Space,Operant'=',Space,Integer]  -> Zuweisung.Integer
# [Name,Space,Operant'=',Space,Name] -> Zuweisung.Variable

# Einfache Operationen "a+=1", "a+=b"
# [Name,Operant'+=',Name]   -> Zuweisung.Addition
# [Name,Operant'+=',Integer]    -> Zuweisung.Addition
# [Name,Operant'*=',Name]   -> Zuweisung.Multiplikation
# [Name,Operant'*=',Integer]    -> Zuweisung.Multiplikation
# [Name,Operant'/=',Name]   -> Zuweisung.Division
# [Name,Operant'/=',Integer]    -> Zuweisung.Division
# [Name,Operant'-=',Name]   -> Zuweisung.Subtraktion
# [Name,Operant'-=',Integer]    -> Zuweisung.Subtraktion
# Einfache Operationen, mit Space: "a += 1", "a += b"
# [Name,Space,Operant'+=',Space,Name]   -> Zuweisung.Addition
# [Name,Space,Operant'+=',Space,Integer]    -> Zuweisung.Addition
# [Name,Space,Operant'*=',Space,Name]   -> Zuweisung.Multiplikation
# [Name,Space,Operant'*=',Space,Integer]    -> Zuweisung.Multiplikation
# [Name,Space,Operant'/=',Space,Name]   -> Zuweisung.Division
# [Name,Space,Operant'/=',Space,Integer]    -> Zuweisung.Division
# [Name,Space,Operant'-=',Space,Name]   -> Zuweisung.Subtraktion
# [Name,Space,Operant'-=',Space,Integer]    -> Zuweisung.Subtraktion

# Einfache Operationen: "a=b+1", "a= a/b", "a=a*1"
# [Name,Operant'=',Name,Operant='+',Integer] -> Zuweisung.Addition
# [Name,Operant'=',Name,Operant='-',Integer] -> Zuweisung.Subtraktion
# [Name,Operant'=',Name,Operant='/',Integer] -> Zuweisung.Division
# [Name,Operant'=',Name,Operant='*',Integer] -> Zuweisung.Multiplikation
# Einfache Operationen, mit Space: "a = a + 1"
# [Name,Space,Operant'=',Space,Name,Operant='+',Space, Integer] -> Zuweisung.Addition
# [Name,Space,Operant'=',Space,Name,Operant='-',Space, Integer] -> Zuweisung.Subtraktion
# [Name,Space,Operant'=',Space,Name,Operant='/',Space, Integer] -> Zuweisung.Division
# [Name,Space,Operant'=',Space,Name,Operant='*',Space, Integer] -> Zuweisung.Multiplikation

# Einfache Operationen, Argumente vertauscht: "a=1+b"
# [Name,Operant'=',Integer,Operant='+',Name] -> Zuweisung.Addition
# [Name,Operant'=',Integer,Operant='-',Name] -> Zuweisung.Subtraktion
# [Name,Operant'=',Integer,Operant='/',Name] -> Zuweisung.Division
# [Name,Operant'=',Integer,Operant='*',Name] -> Zuweisung.Multiplikation
# Einfache Operationen, Argumente vertauscht: "a = 1 + b"
# [Name,Space,Operant'=',Space,Integer,Space,Operant='+',Space,Name] -> Zuweisung.Addition
# [Name,Space,Operant'=',Space,Integer,Space,Operant='-',Space,Name] -> Zuweisung.Subtraktion
# [Name,Space,Operant'=',Space,Integer,Space,Operant='/',Space,Name] -> Zuweisung.Division
# [Name,Space,Operant'=',Space,Integer,Space,Operant='*',Space,Name] -> Zuweisung.Multiplikation


# tbd: ist "Name" ein "Name" oder "Fun_Name"

# if schleifen
#



def tokenize(inputlist):
    chain = [
        ([Parser.Comment], "Kommentar"),  # -> Kommentar
        ([Parser.Name, Parser.Operant, Parser.Integer], "Zuweisung.Integer"),  # -> Zuweisung.Integer
        ([Parser.Name, Parser.Operant, Parser.Name], "Zuweisung.Variable"),  # -> Zuweisung.Variable
        ([Parser.Name, Parser.Space, Parser.Operant, Parser.Space, Parser.Integer], "Zuweisung.Integer"),
        # -> Zuweisung.Integer
        ([Parser.Name, Parser.Space, Parser.Operant, Parser.Space, Parser.Name], "Zuweisung.Variable"),
        # -> Zuweisung.Variable
    ]
    print(inputlist)
    for line in inputlist:
        for objekt in line:
            for ch in chain:
                if objekt == ch:
                    print("ch")
        print("newlne")

    # debug
    outputlist = inputlist

    # Notiz: liste Tupels, nicht 2D: z.B: variable assignment, Variabelname,

    return outputlist
