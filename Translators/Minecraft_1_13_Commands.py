testtokens = [("einfvaridefiinte", ["testint", 2342352]), ("prinvariinte", ["testint"])]

tosetupvariables = []
outlist = []


def translate(tokens, debug=False):
    functions = {"Def.Variable.Integer": defVarInt, "Def.Variable.Variable": defVarVar,
                 "Output.Print.Variable": outPriVar, "Def.Comment": defCom}

    outlist.append("MAIN:")
    for t in tokens:
        if not t[0] in functions:
            print("LOL,", t[0], "can't be translated.")
            continue
        outlist.append(functions[t[0]](t[1]))

    outlist.append("SETUP:")
    for t in tosetupvariables:
        outlist.append("scoreboard objectives add " + t)

    return outlist


def defVarInt(args):
    if not (args[0] in tosetupvariables):
        tosetupvariables.append(args[0])
    return "scoreboard players set Global " + \
           args[0] + " " + \
           str(args[1])


def defVarVar(args):
    if not (args[0] in tosetupvariables):
        tosetupvariables.append(args[0])
    return "scoreboard players operation Global " + args[0] + " = Global" + args[1]


def outPriVar(args):
    return 'tellraw @p ["",{"score":{"name":"Global","objective":' + args[0] + '}}]'


def defCom(args):
    return "# " + args[0]
