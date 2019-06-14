import sys
import time
import ask
import Parser
import Tokenize
import Translators.Minecraft_1_13_Commands as m123c
import argparse
import Translators.Cpp as cpp

parser = argparse.ArgumentParser(description="Programming Language Translator")
parser.add_argument("inputfile", type=str, help="The file, that is going to be translated")
parser.add_argument("outputfile", type=str, help="The output file")
parser.add_argument("outputlanguage", type=str, help="The language that is translated to", choices=["Minecraft_1_13_Commands"])
parser.add_argument("--d", "--debug", type=str, help="Turns debug mode On or off", choices=["on", "off"], default="off")
args = parser.parse_args()

t1 = time.time()
filename = args.inputfile
outputfilename = args.outputfile
debug = bool(args.d.replace("off", "False").replace("on", "True"))
outputlanguage = args.outputlanguage

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
t2 = time.time()
t3 = time.time()
print("Using", outputlanguage + "!")
print("Translating...")
if outputlanguage == "Minecraft_1_13_Commands":
    outcode = m123c.translate(tokens, debug)
print("-" * 20 + "Translation finshed!" + "-" * 20)
a = open(outputfilename, "w")
a.write("")
a.close()
outfile = open(outputfilename, "a")
for line in outcode:
    outfile.write(line + "\n")
outfile.close()
t4 = time.time()
print("-" * 10 + "Timings" + "-" * 10)
tok = t2 - t1
tra = t4 - t3
print("Tokenization took[s]:", tok)
print("Translation took[s] :", tra)
print("Together it took[s] :", tok + tra)
