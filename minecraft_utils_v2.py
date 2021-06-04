from typing import Union
import deployment_engine

Code = list[str]


class MCObjective:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


class MCVar:
    def __init__(self, player: str, objective: MCObjective = MCObjective("global"), dtype: MCClass = MCInt):
        self.player = player
        self.objectve = objective
        self.dtype = dtype

    def __str__(self):
        return f"{self.player} {self.objectve}"


class MCClass:
    def __init__(self):
        self.attrs = set()
        self.functions: list["MCFunction"] = []

        self.magic_functions: dict[str: Union[MCFunction, None]] = {"__init__": None,
                                                                    "__tick__": None,
                                                                    "__load__": None}

    def set_init(self, function: "MCFunction" = None):
        self.magic_functions["__init__"] = function

    def add_function(self, function: "MCFunction"):
        self.functions.append(function)

    # self.attrs.update(function.get_vars())


from mctpyes import *


def pp_code(files: dict[str: Code]) -> str:
    return "\n\n".join([f"[{file}.mcfunction]\n" + "\n".join(files[file]) for file in files])


class MCCompiler:
    def __init__(self, namespace: str):
        self.namespace = namespace
        self.main: Union[MCFunction, None] = None

    def get_code(self) -> dict[str: Code]:
        """Returns a dict of mcfunction filenames and code"""


class MCMain(MCClass):
    def __init__(self, compiler: MCCompiler, name: str = "__main__"):
        super().__init__(name)


class MCFunction:
    def __init__(self, compiler: MCCompiler):
        self.commands: Code = []
        self.vars: set[MCVar] = set()

    def add_command(self, command: str):
        """Appends the minecraft command specified to the command list"""
        self.commands.append(command)

    def get_code(self):
        return self.commands

    def get_vars(self):
        return self.vars

    def create_object(self, mcclass: MCClass):
        # calls create_object backend function
        ...
