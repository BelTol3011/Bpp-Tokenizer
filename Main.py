import sys
import Parser
import Tokenize
import Translators.Minecraft_1_13_Commands as translator


# Kriegt Dateinamen un outputnamen als Argumente.
# ZU kompiliertem File
#  - Parsen
#  - Tokenize
#  - Kompilieren

arguments = sys.argv

#print(arguments)

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
tokenized = Tokenize.tokenize(parsed)
#print(tokenized)