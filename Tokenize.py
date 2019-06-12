import sys
import Parser

arguments = sys.argv
debugflag = True

def tokenize(Inputlist):

  #  chain = [
  #     (["Comment"], "Kommentar"),                             # -> Kommentar
  #      (["Name", "Operant", "Integer"], "Zuweisung.Integer"),  # -> Zuweisung.Integer
  #      (["Name", "Operant", "Name"], "Zuweisung.Variable"),    # -> Zuweisung.Variable
  #      (["Name", "Operant", "String"], "Zuweisung.String")     # -> Zuweisung.String
  #  ]

    SyntaxChain = [
        ([("Comment",""),("",""),("","")], "Def.Comment"),
        ([("Name", ""), ("Operant",  "="), ("Integer", "")], "Def.Variable.Integer"),
        ([("Name", ""), ("Operant",  "="), ("Name", "")],    "Def.Variable.Variable"),

        ([("Name", ""), ("Operant",  "="), ("Boolean", "")], "Zuweisung.Variable.Bool.Simple"),
        ([("Name", ""), ("Operant",  "="), ("String", "")],  "Zuweisung.Variable.String.Simple"),
        ([("Name", ""), ("Operant", "+="), ("Integer", "")], "Zuweisung.Variable.Integer.Add"),
        ([("Name", ""), ("Operant", "-="), ("Integer", "")], "Zuweisung.Variable.Integer.Subst"),
        ([("Name", ""), ("Operant", "/="), ("Integer", "")], "Zuweisung.Variable.Integer.Divide"),
        ([("Name", ""), ("Operant", "*="), ("Integer", "")], "Zuweisung.Variable.Integer.Multiply")
    ]


#([("Comment", ""), ("", ""), ("", "")], "Kommentar"),
#([("Name", ""), ("Operant", "="), ("Integer", "")], "Definition.Variable.Integer"),
#([("Name", ""), ("Operant", "="), ("Name", "")], "Definition.Variable.Variable"),
#([("Name", "print"), ("Parentheses", "("), ("Name", ""), ("Parentheses", ")")], "Output.Print.Variable")([("Comment",""),("",""),("","")], "Kommentar"),
# ([("Name", ""), ("Operant",  "="), ("Integer", "")], "Definition.Variable.Integer"),
# ([("Name", ""), ("Operant", "="), ("Name", "")], "Definition.Variable.Variable"),
# ([("Name", "print"), ("Parentheses", "("), ("Name", ""), ("Parentheses", ")")], "Output.Print.Variable")









    for InputElementIndex in range(0, len(Inputlist)):  # Line
        print("bpp-ScriptZeile: ", InputElementIndex, " ", Inputlist[InputElementIndex])
        type = "No type found"    #Ausgangszustand
        #InputElementIndex = 0
        for ChainIndex in range(0, len(SyntaxChain)):
            #print(SyntaxChain[ChainIndex][0][0], "  ", Inputlist[InputElementIndex])
            if Inputlist[InputElementIndex][0].type == SyntaxChain[ChainIndex][0][0][0]:
                #print("...")
                type = SyntaxChain[ChainIndex][1] #ergebnis
                break







            #print(SyntaxChain[ChainIndex][0][InputElementIndex][0])
            #print(Inputlist[InputElementIndex].type)

            #if SyntaxChain[ChainIndex][0][0][0] == Inputlist[InputElementIndex].type:
             #   print(SyntaxChain[ChainIndex][0][0][0])
              #  type = SyntaxChain[ChainIndex][1]
                #break

         #   if len(Inputlist[InputElementIndex]) == len(chain[ChainZeilenIndex][0]):
         #      #print(chain[ChainZeilenIndex][0], " ", len(Inputlist[InputElementIndex]), " ", len(chain[ChainZeilenIndex][0]))
         #      canceled = True
         #   for InputElementIndex in range(0, len(Inputlist[InputElementIndex])):
                    # print(Inputlist[InputElementIndex][InputZeilenElementIndex].type)
                  # print(SyntaxChain[ChainZeilenIndex][0][0][0])
                  # if Inputlist[InputElementIndex][InputZeilenElementIndex].type != SyntaxChain[ChainZeilenIndex][0][InputZeilenElementIndex][0]:
                  #      canceled = False  #wenn noch nicht gefunden, wird nicht abgebrochen
                  #      break
               # if canceled:
                #   type = SyntaxChain[ChainIndex][0][0][0]

        print("-->", type)
        print("---------------------")

    # outputlist = Inputlist
    # Notiz: liste Tupels, nicht 2D: z.B: variable assignment, Variabelname,

    return []



#    print(Inputlist)
#    for InputElementIndex in range(0, len(Inputlist)):  # Line
#        print("Zeile: ", InputElementIndex," ",Inputlist[InputElementIndex], "| Inputline")
#        type = "No type found"
#        for ChainZeilenIndex in range(0, len(chain)):#
#            if len(Inputlist[InputElementIndex]) == len(chain[ChainZeilenIndex][0]):
#                #print(chain[ChainZeilenIndex][0], " ", len(Inputlist[InputElementIndex]), " ", len(chain[ChainZeilenIndex][0]))
#                canceled = True
#                for InputZeilenElementIndex in range(0, len(Inputlist[InputElementIndex])):
#                    if Inputlist[InputElementIndex][InputZeilenElementIndex].type != chain[ChainZeilenIndex][0][InputZeilenElementIndex]:
#                        canceled = False
#                        break
#                if canceled:
#                    type = chain[ChainZeilenIndex][1]#
#
#        print("-->", type)
#        print("---------------------")



# Strg+Alt+L : Reformat
##
# Aufgaben:
# bekommt eine 2D-Liste, geschachtelt mit Tupels
# In Tokens umwandeln:
# Die Objekttypen sind vom parser übergeben worden
# die tokenize funktion beschreibt durch logische KOmbination der Tupels die Sprachkonstrukte
# Zuletzt die Liste mit dump in eine datei speichern

# Objektfolgen:
# [Comment] -> Kommentar
# [Name,Operant'=',Integer]     -> Zuweisung.Integer
# [Name,Operant'=',Name]        -> Zuweisung.Variable

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