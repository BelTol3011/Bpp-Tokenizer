import sys
import time
import ask
import Parser
import Tokenize
import Translators.Minecraft_1_13_Commands as m123c
import Translators.Cpp as cpp

debug = False

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
t1 = time.time()
print("Converting", filename, "to", outputfilename + ".")
if debug: print("Opening File...")
infile = open(filename)
inlist = infile.read().split("\n")
if debug: print("Parsing...")
parsed = Parser.Pars(inlist, debug)
if debug: print("Tokenizing...")
tokens = Tokenize.tokenize(parsed, debug)
if tokens == [] or tokens == "":
    raise Exception("Output of the tokenization is empty. Interrupting!")
if debug: print(tokens)
print("-" * 10 + "Tokenization finshed!" + "-" * 10)
modules = [m123c]
modulna = ["Minecraft 1.13 Commands"]
modulen = ["1"]
print("1 Minecraft 1.13 Commands(Maybe works for 1.14)")
t2 = time.time()
translator = ask.ask(["1"])
t3 = time.time()
i = modulen.index(translator)
print("Using", modulna[i - 1] + "!")
print("Translating...")
outcode = modules[i - 1].translate(tokens, debug)
print("-" * 20 + "Translation finshed!" + "-" * 20)
for line in outcode:
    print(line)
t4 = time.time()
print("-" * 10 + "Timings" + "-" * 10)
tok = t2 - t1
tra = t4 - t3
print("Tokenization took[s]:", tok)
print("Translation took[s] :", tra)
print("Together it took[s] :", tok + tra)
