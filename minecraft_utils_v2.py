from typing import Union
import deployment_engine
import mc_command_wrapper as mccw

Code = list[str]


class MCPrimitiveVar:
    def __init__(self, function: "MCFunction", player: str, objective: str):
        self.function = function
        self.player = player
        self.objective = objective

    def set(self, value: int):
        self.function.add_command(mccw.set_score(self.player, self.objective, value))

    def add(self, value: int):
        self.function.add_command(mccw.score_add_const(self.player, self.objective, value))

    def __str__(self):
        return f"{self.player}@{self.objective}"

    def print(self):
        # TODO: Create tellraw generator library
        self.function.add_command(mccw.print_score(self.player, self.objective), f"print({self})")


class MCClass:
    def __init__(self):
        self.attrs = set()
        self.functions: list["MCFunction"] = []

        self.magic_functions: dict[str: Union[MCFunction, None]] = {"__init__": None, "__load__": None}


from mctpyes import *


def pp_code(files: dict[str: Code]) -> str:
    return "\n".join([f"[{file}.mcfunction]\n" + "\n".join(files[file]) for file in files])


class Namespace:
    def __init__(self, namespace: str):
        self.namespace = namespace
        self.functions: list[MCFunction] = []

    def create_function(self, *args, **kwargs):
        function = MCFunction(*args, **kwargs)
        self.functions.append(function)
        return function

    def get_code(self) -> Code:
        return sum([function.get_function_list() for function in self.functions], [])


class MCFunction:
    def __init__(self, name: str):
        self.commands: Code = []
        self.name = name

    def get_function_list(self) -> Code:
        return [f"### {self.name}"] + self.commands

    def get_objective(self):
        # TODO: Return unique identifier if name of function is longer thn 16
        return self.name

    def get_code(self):
        return self.commands

    def get_var(self, name: str, scope: Union[Namespace, "MCFunction", str] = None):
        scope = self if scope is None else scope

        if isinstance(scope, str):
            objective = scope
        else:
            objective = scope.get_objective()

        return MCPrimitiveVar(self, name, objective)

    def create_object(self, mcclass: MCClass):
        # calls create_object backend function
        # self.call_mc
        ...

    def add_command(self, command: str, comment: str = ""):
        """Appends the minecraft command specified to the command list"""
        if comment:
            self.commands.append(f"# {comment}")
        else:
            # TODO: standardize warnings
            print(f"Warning: No comment provided for the following command: `{command}`")
        self.commands.append(command)

    def add_commands(self, commands: list[str]):
        """Appends a list of commands and premises to the command list"""

        for command in commands:
            if command is None:
                continue
            self.add_command(command)

    def say(self, message: str):
        self.add_command(f"say {message}")
