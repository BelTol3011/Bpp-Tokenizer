debugflag = True


# strg+alt+L

def tokenize(Inputlist):
    SyntaxChain = [
        ([("Comment", "")], "Def.Comment", [0]),
        ([("Name", ""), ("Operant", "="), ("Integer", "")], "Def.Variable.Integer", [0, 2]),
        ([("Name", ""), ("Operant", "="), ("Name", "")], "Def.Variable.Variable", [0, 2]),
        ([("Name", "print"), ("Parentheses", "("), ("Name", ""), ("Parentheses", ")")], "Output.Print.Variable", [2])
    ]
    outlist = []
    debug = debugflag
    for ZeilenIndex in range(0, len(Inputlist)):
        print("Zeile:", Inputlist[ZeilenIndex])
        outTok = "No Type Found!"

        for SyntaxChainIndex in range(0, len(SyntaxChain)):
            if debug: print(SyntaxChain[SyntaxChainIndex][0])
            if debug: print("Comparing:", len(Inputlist[ZeilenIndex]), len(SyntaxChain[SyntaxChainIndex][0]))
            if len(Inputlist[ZeilenIndex]) == len(SyntaxChain[SyntaxChainIndex][0]):
                works = True
                for ObjectAndSyntaxChainIndex in range(0, len(Inputlist[ZeilenIndex])):
                    if debug: print("ObjectAndSyntaxChainIndex", ObjectAndSyntaxChainIndex)
                    currentZeilenObject = Inputlist[ZeilenIndex][ObjectAndSyntaxChainIndex]
                    currentSyntaxObject = SyntaxChain[SyntaxChainIndex][0][ObjectAndSyntaxChainIndex]
                    if currentSyntaxObject[0] != "":
                        if currentSyntaxObject[0] != currentZeilenObject.type:
                            works = False
                    if currentSyntaxObject[1] != "":
                        if currentSyntaxObject[1] != currentZeilenObject.data:
                            works = False
                if works:
                    outTok = SyntaxChain[SyntaxChainIndex][1]
                    for RegelIndex in range(0, len(SyntaxChain)):
                        if SyntaxChain[RegelIndex][1] == outTok:
                            outTokindex = RegelIndex
                    if debug: print("OutTokIndex", outTokindex)

                    if debug: print("Regel", outTok, "funktioniert!")
                    if debug: print("searching arguments...")
                    args = []
                    for ArgIndex in SyntaxChain[outTokindex][2]:
                        args.append(Inputlist[ZeilenIndex][ArgIndex].data)
                    if debug: print("Args:", args)
                    outlist.append((outTok, args))
            else:
                if debug: print("Lengths don't match up!")
            if debug: print("-"*5 + "Next Syntax" + "-"*5)
        print(outTok)
    return outlist

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
