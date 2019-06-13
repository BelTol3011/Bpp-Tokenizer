testtokens = [("einfvaridefiinte", ["testint", 2342352]), ("prinvariinte", ["testint"])]

def translate():
    pass


def einfvaridefiinte(*args):
    args = args[0]
    if not (args[0] in tosetupvariables):
        tosetupvariables.append(args[0])
    return "scoreboard players set Global " + \
           args[0] + " " + \
           str(args[1])


def prinvariinte(*args):
    args = args[0]
    return 'tellraw @p ["",{"score":{"name":"Global","objective":' + args[0] + '}}]'


tosetupvariables = []
functions = {"einfvaridefiinte": einfvaridefiinte, "prinvariinte": prinvariinte}
outlist = []
for t in testtokens:
    outlist.append(functions[t[0]](t[1]))

print("setup")
for t in tosetupvariables:
    print("scoreboard objectives add " + t)
print("main")
for o in outlist:
    print(o)
