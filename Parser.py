class Operant:
    type = "Operant"

    def __init__(self, type):
        self.data = type


class Boolean:
    type = "Boolean"

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


class Calc_Operant:
    type = "Calc_Operant"

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


class Parentheses:
    type = "Parentheses"

    def __init__(self, paran):
        self.data = paran


class String:
    type = "String"

    def __init__(self, paran):
        self.data = paran


class Float:
    type = "Float"

    def __init__(self, paran):
        self.data = paran


class Dot:
    type = "Dot"

    def __init__(self, paran):
        self.data = paran


class Seperator:
    type = "Seperator"

    def __init__(self, paran):
        self.data = paran


def is_type(x):
    if x in operants:
        return "operant"
    elif x in compare_operants:
        return "compare_Operant"
    elif x in calc_operants:
        return "calc_Operant"
    elif x == " " or x == "":
        return "space"
    elif x in "()":
        return "parants"
    elif x in "1234567890":
        return "integer"
    elif x == ".":
        return "dot"
    elif x == "\"":
        return "quot_mark"
    elif x == "#":
        return "comment"
    elif x == "," or x == ";":
        return "seperator"
    else:
        return "name"


classregister = {"operant": Operant, "compare_Operant": Compare_Operant, "name": Name, "space": Space,
                 "parants": Parentheses, "integer": Integer, "comment": Comment, "string": String, "dot": Dot,
                 "calc_Operant": Calc_Operant, "seperator": Seperator, "bool": Boolean}
operants = ["=", "-=", "+=", "*=", "/=", "%=", "++", "--"]
compare_operants = ["or", "and", "not"]
calc_operants = ["+", "-", "*", "/", "%"]


def concatenate(input_list):
    output_list = []
    i = -1
    input_list.append("")
    string = False
    stringstring = ""
    while i < len(input_list):
        i += 1
        temp = ""
        current_letter = input_list[i]
        current_type = is_type(current_letter)
        if string and current_type == "quot_mark":
            string = False
            stringstring += current_letter
            output_list.append(("string", stringstring))
            # print(1)
            continue
        if current_type == "quot_mark":
            string = True
            stringstring += current_letter
            continue
        if string:
            stringstring += current_letter
            continue

        if current_letter == "#" and (not string):
            del input_list[0]
            if input_list[0] == " ":
                del input_list[0]
            comment = "".join(input_list)
            output_list.append(("comment", comment))
            break

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
        # i += 1
    return output_list


def Pars(inlist, debug=False):
    # print(inlist)
    _outlist = []
    for line in inlist:
        _outlist.append(concatenate(list(line)))

    if debug: print(_outlist)
    outlist = []
    for line in _outlist:
        temp = []
        for tupel in line:
            type = tupel[0]
            arg = tupel[1]
            # print(arg)
            temp.append(classregister[type](arg))
        outlist.append(temp)

    # floating
    if debug: print("concatenating floats..")
    for i in range(0, len(outlist)):
        for j in range(1, len(outlist[i]) - 1):

            if outlist[i][j - 1].type == "Integer" and outlist[i][j].type == "Dot" and outlist[i][j + 1].type == \
                    "Integer":
                outlist[i][j] = Float(float(str(outlist[i][j - 1].data) + "." + str(outlist[i][j + 1].data)))
                del outlist[i][j + 1]
                del outlist[i][j - 1]

    if debug: print("concatenating operants...")
    for i in range(0, len(outlist)):
        for j in range(0, len(outlist[i]) - 1):
            if outlist[i][j].data \
                    == "-" and outlist[i][j + 1].data == \
                    "=":
                outlist[i][j] = Operant("-=")
                del outlist[i][j + 1]
            elif outlist[i][j].data \
                    == "+" and outlist[i][j + 1].data == \
                    "=":
                outlist[i][j] = Operant("+=")
                del outlist[i][j + 1]
            elif outlist[i][j].data \
                    == "*" and outlist[i][j + 1].data == \
                    "=":
                outlist[i][j] = Operant("*=")
                del outlist[i][j + 1]
            elif outlist[i][j].data \
                    == "/" and outlist[i][j + 1].data == \
                    "=":
                outlist[i][j] = Operant("/=")
                del outlist[i][j + 1]
            elif outlist[i][j].data \
                    == "%" and outlist[i][j + 1].data == \
                    "=":
                outlist[i][j] = Operant("%=")
                del outlist[i][j + 1]

    if debug: print("detecting bools...")
    for i in range(0, len(outlist)):
        for j in range(0, len(outlist[i])):
            if outlist[i][j].data in ["True", "False"]:
                outlist[i][j] = Boolean(outlist[i][j].data)

    if debug: print("removing spaces...")
    new_outlist = []
    for i in range(0, len(outlist)):
        temp = []
        for j in range(0, len(outlist[i])):
            if outlist[i][j].type != "Space":
                temp.append(outlist[i][j])
        new_outlist.append(temp)
    outlist = new_outlist

    for line in outlist:
        if debug: print()
        for element in line:
            if debug: print(element.type, element.data, end=", ")
    if debug: print()
    return outlist
