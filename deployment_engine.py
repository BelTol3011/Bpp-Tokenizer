Code = list[str]


# Path = tuple[str, list[str]]

class Path(tuple[str, list[str]]):
    def __hash__(self):
        return hash(get_mcfunction_str(self))


def get_mcfunction_str(path: Path):
    path_str = "/".join(path[1])
    return f"{path[0]}:{path_str}"


def split_list_file(input_code: Code) -> dict[str: Code]:
    """Splits a .list.mcfunction file into seperate functions and returns their location"""

    section_indices = [i for i, line in enumerate(input_code) if line.startswith("###")] + [-1]

    sections = {}
    for i in range(len(section_indices) - 1):
        current = section_indices[i]
        next_ = section_indices[i + 1]
        section = input_code[current + 1:next_]

        name = input_code[current].rstrip().split()[-1]

        sections.update({name: section})

    return sections


def karma_util(string: str, search_char: str = "$") -> list[int]:
    """
    Searches a string for the search_char with attention to parentheses and stuff.
    :param string: the string to be scanned
    :param search_char: the char that is searched for in `string`
    :return: the list of indeces in `string` that match `search_char` with attention to parentheses and stuff
    """
    assert len(search_char) == 1
    indeces = []

    in_string = False
    in_comment = False
    karma = 0
    for i, char in enumerate(string):
        if char in "({[":
            karma += 1
        elif char in ")}]":
            karma -= 1
        elif char == '"':
            in_string = not in_string
        elif char == "#" and not in_string:
            in_comment = True
        elif char == "\n":
            in_string = False
            in_comment = False
            karma = 0

        if karma == 0 and not in_string and char == search_char and not in_comment:
            indeces.append(i)

    return indeces


def link(code: Code, function_dict: dict[str: tuple[Path, Code]]) -> Code:
    """replaces the function tag $function with the real function path namespace:.../function
    Example ( namespace="namespace", function_dict={"mcutils": ["mcutils", "create_object"]} ):
        $foo -> namespace:path/.../foo
        $create_obj@mcutils -> namespace:mcutils/create_obj
    """

    # convert Code to str
    code = "\n".join(code)

    indeces = karma_util(code, "$")  # indeces of the $ symbols in the file string
    # print(f"{indeces=}")
    for index in indeces:
        name = ""
        i = 1
        while len(code) > index + i and (char := code[index + i]) not in [" ", "\n"]:
            name += char
            i += 1

        if code[index - 1] != "\n":
            replacement = get_mcfunction_str(function_dict[name][0])
        else:
            code_ = link(function_dict[name][1], function_dict)
            replacement = f"##! [{name}] begin\n" + "\n".join(code_) + f"\n##! [{name}] end\n"
        # print(mcfunction_string)
        code = code[:index] + replacement + code[index + len(replacement):]

    return code.split("\n")


def batch_link(function_lists: list[tuple[Path, Code]]):
    """
    :param function_lists: A list of Paths and .list.mcfunction files
    :return:
    """
    functions_namescodes: dict[str: tuple[Path, Code]] = {}
    print("Splitting...")
    for path, function_list in function_lists:
        print(f"\t{get_mcfunction_str(path)}")
        _functions = split_list_file(function_list)

        for name in _functions:
            print(f"\t\t{name}")
            # functions_code.update({name: _functions[name]})
            # extend the path to contain the function name
            _path = Path((path[0], path[1] + [name]))
            functions_namescodes.update({name: (_path, _functions[name])})

    print("Linking...")

    # link
    linked_functions: dict[Path: Code] = {}
    for name in functions_namescodes:
        path, code = functions_namescodes[name]
        print(f"\t{get_mcfunction_str(path)}")

        linked_code = link(code, functions_namescodes)

        linked_functions.update({path: linked_code})

    print("Listing:")
    for path in linked_functions:
        print(f"==> {get_mcfunction_str(path)}")
        print("\n".join(linked_functions[path]))


def main():
    """How to compile:
    1. split, link and copy libmcutils into the 'mcutils' path
    2. generate the unlinked user code (.list.mcfunction) via the python script
    3. link and copy the user code with the mcutils function locations
    """
    with open("mcutils/mcutils.list.mcfunction", "r") as f:
        code = f.read().split("\n")
    batch_link([(Path(("mcutils", [])), code)])


if __name__ == "__main__":
    main()
