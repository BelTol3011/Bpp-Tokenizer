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
        (["Comment", "Name"], "Kommentar"),  # -> Kommentar
        (["Name", "Operant", "Integer"], "Zuweisung.Integer"),  # -> Zuweisung.Integer
        (["Name", "Operant", "Name"], "Zuweisung.Variable"),  # -> Zuweisung.Variable
        (["Name", "Space", "Operant", "Space", "Integer"], "Zuweisung.Integer"),
        # -> Zuweisung.Integer
        ([Parser.Name, Parser.Space, Parser.Operant, Parser.Space, Parser.Name], "Zuweisung.Variable"),
        # -> Zuweisung.Variable
    ]

    # print(inputlist)
    for InputZeilenIndex in range(0, len(inputlist)):  # Line
        print(inputlist[InputZeilenIndex], "| Inputline")

        for ChainZeilenIndex in range(0, len(chain)):

            if len(inputlist[InputZeilenIndex]) == len(chain[ChainZeilenIndex][0]):
                print(chain[ChainZeilenIndex][0], " ", len(inputlist[InputZeilenIndex]), " ", len(chain[ChainZeilenIndex][0]))
                for InputZeilenElementIndex in range(0, len(inputlist[InputZeilenIndex])):
                    if inputlist[InputZeilenIndex][InputZeilenElementIndex].type != chain[ChainZeilenIndex][0][InputZeilenElementIndex]:
                        print("Skip")
                        break
                    else: #InputZeilenElementIndex == len(inputlist[InputZeilenIndex]):
                        print("-->", chain[ChainZeilenIndex][1])
        print("---------------------")

    # outputlist = inputlist

    # Notiz: liste Tupels, nicht 2D: z.B: variable assignment, Variabelname,

    return ""
