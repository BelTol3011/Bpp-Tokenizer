import Tokenize

operants = ["=", "-=", "+=", "*=", "/=", "%=", "++", "--"]
compare_operants = ["or", "and", "not"]
calc_operants = ["+", "-", "*", "/", "%"]


def is_type(x):
    if x in operants: return "Operant"
    if x in compare_operants: return "Compare_Operant"


class Operant():
    type = "Operant"

    def __init__(self, type):
        self.data = type


class Compare_Operant():
    type = "Compare_Operant"

    def __init__(self, type):
        self.data = type


class Name():
    type = "Name"

    def __init__(self, name):
        self.data = name


class Integer():
    type = "Integer"

    def __init__(self, int):
        self.data = int


class Comment():
    type = "Comment"

    def __init__(self, comment):
        self.data = comment


def concatenate(input_list):
    output_list = []
    i = 0

    input_list.append("")

    while i < len(input_list):
        temp = ""
        current_letter = input_list[i]
        current_type = is_type(current_letter)
        print(current_letter, current_type)
        if current_letter == "":
            break
        for j in range(i, len(input_list)):
            if input_list[j] == current_letter:
                temp += input_list[j]
            else:
                upto = j
                break
        output_list.append(temp)
        i = upto - 1
        i += 1
    return output_list


def Pars(inlist):
    print(inlist)
    print(concatenate(list(inlist[0])))


testlist = [
    [Name("a"), Operant("="), Integer(1)]
]

Tokenize.tokenize(testlist)
