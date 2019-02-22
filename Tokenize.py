import sys
import dump

arguments = sys.argv

# Strg+Alt+L : Reformat

# Aufgaben:
# bekommt eine 2D-Liste, geschachtelt mit Tupels
# ({Argument1}{Obj1})
# ({Argument2}{Obj2})
#
# - File in tokens umwandeln
# - In eine dump datei speichern
#
#
testliste = [
    ['a']['Variable'],
    ['=']['Operator'],
    ['1'][''],
]


def tokenize(inputliste):
    for line in inputliste:
        print()

    # endfor
