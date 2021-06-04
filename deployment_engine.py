from typing import Literal

Code = list[str]
Path = list[str]


def get_mcfunction_str(namespace: str, path: Path):
    path_str = "/".join(path)
    return f"{namespace}:{path_str}"


def split_list_file(input_code: Code) -> dict[str: Code]:
    """Splits a .list.mcfunction file into seperate functions and returns their location"""

    section_indices = [i for i, line in enumerate(input_code) if line.startswith("###")] + [-1]

    sections = {}
    for i in range(len(section_indices) - 1):
        current = section_indices[i]
        next_ = section_indices[i + 1]
        section = input_code[current:next_]

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
    karma = 0
    for i, char in enumerate(string):
        if char in "({[":
            karma += 1
        elif char in ")}]":
            karma -= 1
        elif char == '"':
            in_string = not in_string

        if karma == 0 and not in_string and char == search_char:
            indeces.append(i)

    return indeces


def link(code: Code, function_dict: dict[str: Path]) -> Code:
    """replaces the function tag $function with the real function path namespace:.../function
    Example ( namespace="namespace", function_dict={"mcutils": ["mcutils", "create_object"]} ):
        $foo -> namespace:path/.../foo
        $create_obj@mcutils -> namespace:mcutils/create_obj
    """

    # convert Code to str
    code = "\n".join(code)

    indeces = karma_util(code, "$")  # indeces of the $ symbols in the file string
    print(f"{indeces=}")


def _to_datapack(functions: list[Code], libmcutils: Code, libmcutils_prefix: Path):
    """
    :param functions: The .list.mcfunction file of all functions
    :param libmcutils: The code for the libmcutils library
    :param libmcutils_prefix: The path to libmcutils in the datapack
    :return:
    """
    print("Splitting...")

    files = split_list_file(libmcutils)

    files = split_list_file(libmcutils)

    print("Finished!")
    print("Linking libmcutils...")

    # generate function name dict
    function_dict: dict[str: Path] = {}
    for file in files:
        function_dict.update({file: libmcutils_prefix + [file]})

    # link
    linked_functions: dict[str: Code] = {}
    for function in functions:
        print(f"linking {function}...", end="")

        linked_code = link(functions[function], function_dict)

        linked_functions.update({f})


if __name__ == "__main__":
    """How to compile:
    1. split, link and copy libmcutils into the 'mcutils' path
    2. generate the unlinked user code (.list.mcfunction) via the python script
    3. link and copy the user code with the mcutils function locations
    """
    split_list_file()
