import sys
import time

import Parser
import Tokenize
import ask

t1 = time.time()

# Kriegt Dateinamen un outputnamen als Argumente.
# ZU kompiliertem File
#  - Parsen
#  - Tokenize
#  - Kompilieren

arguments = sys.argv

# print(arguments)

if arguments[0] == "python" or arguments[0] == "python3": del arguments[0]

filename = arguments[1]
outputfilename = arguments[2]

print("Converting", filename, "to", outputfilename + ".")
print("Opening File...")
infile = open(filename)
inlist = infile.read().split("\n")
print("Parsing...")
parsed = Parser.Pars(inlist)
print("Tokenizing...")
tokens = Tokenize.tokenize(parsed)
if tokens == [] or tokens == "":
    raise Exception("Output of the tokenization is empty. Interrupting!")
print("------------------------")
print("Time Elapsed: ", time.time() - t1)
print(tokens)
print("Everything Tokenized!")
modules = ["Minecraft_1_13_Commands"]
modulen = ["1"]
print("1 Minecraft 1.13 Commands(Maybe works for 1.14)")
translator = ask.ask(["1"])
i = modulen.index(translator)
print("Using", modules[i] + "!")
tr = __import__("Translators." + modules[i])
print("Translating...")
outcode = tr.translate(tokens)
for line in outcode:
    print(line)

# a = [
#    ([("Name", "any"), ("Operant", "="), ("Integer", "any")], "einfvaridefiinte")
# ]
