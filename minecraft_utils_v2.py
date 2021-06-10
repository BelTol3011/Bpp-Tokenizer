from typing import Union, Literal
import deployment_engine
import mc_command_wrapper as mccw

Code = list[str]
META_OBJECTIVE = "__mcutils__"
RETURN_PLAYER = "ret"


class MCPrimitiveVar:
    def __init__(self, function: "MCFunction", player: str, objective: str):
        # TODO: make sure objective is valid
        self.function = function
        self.player = player
        self.objective = objective

    def set(self, value: int):
        self.function.add_command(mccw.score_set_cons(self.player, self.objective, value), f"{self} = {value}")

    def add(self, value: int):
        self.function.add_command(mccw.score_add_const(self.player, self.objective, value), f"{self} += {value}")

    def __str__(self):
        return f"{self.player}@{self.objective}"

    def print(self):
        # TODO: Create tellraw generator library
        self.function.add_command(mccw.print_score(self.player, self.objective), f"print({self})")

    def call_function(self, function: "MCFunction", *arguments: "MCPrimitiveVar"):
        # TODO: maybe implement library requirement system
        # push arguments to stack
        for argument in arguments:
            self.function.add_command(mccw.score_set("arg", "mcutils", argument.player, argument.objective),
                                      f"set arg {argument} for mcutils push operation")
            self.function.add_command(mccw.call_function("push"), "invoke mcutils push operation")
        self.function.add_command(mccw.call_function(function.name), f"call {function.name} function")


class MCClass:
    def __init__(self):
        self.functions: list["MCFunction"] = []


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
    def __init__(self, name: str, *arguments: MCPrimitiveVar):
        self.commands: Code = []
        self.name = name
        # reverse arguments because first arguments are pushed first so the last argument is the first to be popped
        arguments = list(arguments)
        arguments.reverse()
        for argument in arguments:
            # pop
            self.add_command(mccw.call_function("pop"), f"pop {argument}")

            # TODO: switch context to this function
            # define var
            self.add_command(mccw.score_set(argument.player, argument.objective, "ret", "mcutils"), "finish pop")

    def get_function_list(self) -> Code:
        return [f"### {self.name}"] + self.commands

    def get_player(self):
        # mcfunctions are static so this is constant
        return f"{self.name}_func"

    def get_code(self):
        return self.commands

    def return_(self, var: Union[MCPrimitiveVar]):
        # set return score
        self.add_command(mccw.score_set(RETURN_PLAYER, META_OBJECTIVE, var.player, var.objective), f"return {var}")

    def get_var(self, name: str, scope: Union[Namespace, "MCFunction", str] = None):
        scope = self if scope is None else scope

        if scope == "self":
            player = "@e[tag=mcutils.ret, limit=1]"
        elif isinstance(scope, str):
            player = scope
        else:
            player = scope.get_player()

        return MCPrimitiveVar(self, player, name)

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
            print(f"Warning: No comment provided: `{command}`")
        self.commands.append(command)

    def add_commands(self, commands: list[str]):
        """Appends a list of commands and premises to the command list"""
        # TODO: make comments able to be disabled
        for command in commands:
            if command is None:
                continue
            self.add_command(command)

    def say(self, message: str):
        self.add_command(f"say {message}", f"print(\"{message}\")")
