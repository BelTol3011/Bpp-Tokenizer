import Tokenize

class Operant():
    type = "Operant"
    def __init__(self, type):
        self.data = type

class Variable_Name():
    type = "Var_Name"
    def __init__(self, name):
        self.data = name

class Integer():
    type = "integer"
    def __init__(self, int):
        self.data = int


testlist = [
    [Variable_Name("a"),Operant("="),Integer(1)]
]

Tokenize.tokenize(testlist)