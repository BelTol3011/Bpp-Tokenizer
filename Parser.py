import Tokenize


class Operant:
    type = "Operant"

    def __init__(self, type):
        self.data = type


class Space:
    type = "Space"

    def __init__(self, space=" "):
        self.data = space


class Compare_Operant:
    type = "Compare_Operant"

    def __init__(self, type):
        self.data = type


class Name:
    type = "Name"

    def __init__(self, name):
        self.data = name


class Integer:
    type = "Integer"

    def __init__(self, int):
        self.data = int


class Comment:
    type = "Comment"

    def __init__(self, comment):
        self.data = comment


class Parantheses:
    type = "Parantheses"

    def __init__(self, paran):
        self.data = paran


def is_type(x):
    if x in operants:
        return "Operant"
    elif x in compare_operants:
        return "Compare_Operant"
    elif x == " " or x == "":
        return "space"
    elif x in "()":
        return "parants"
    elif x in "1234567890":
        return "integer"
    else:
        return "name"


classregister = {"Operant": Operant, "Compare_Operant": Compare_Operant, "name": Name, "space": Space,
                 "parants": Parantheses, "integer": Integer}
operants = ["=", "-=", "+=", "*=", "/=", "%=", "++", "--"]
compare_operants = ["or", "and", "not"]
calc_operants = ["+", "-", "*", "/", "%"]


def concatenate(input_list):
    output_list = []
    i = 0

    input_list.append("")

    while i < len(input_list):
        temp = ""
        current_letter = input_list[i]
        current_type = is_type(current_letter)
        # print(current_letter, current_type)
        if current_letter == "":
            break
        for j in range(i, len(input_list)):
            if is_type(input_list[j]) == is_type(current_letter):
                temp += input_list[j]

            else:
                # temp += input_list[j]
                upto = j
                break

        output_list.append((current_type, temp))
        i = upto - 1
        i += 1
    return output_list


def Pars(inlist):
    # print(inlist)
    _outlist = []
    for line in inlist:
        _outlist.append(concatenate(list(line)))

    #print(_outlist)
    outlist = []
    for line in _outlist:
        temp = []
        for tupel in line:
            type = tupel[0]
            arg = tupel[1]
            # print(arg)
            temp.append(classregister[type](arg))
        outlist.append(temp)
    return outlist
