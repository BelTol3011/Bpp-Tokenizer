from typing import Union, Literal
import deployment_engine
import mc_command_wrapper as mccw

Code = list[str]
META_OBJECTIVE = "__mcutils__"
RETURN_PLAYER = "ret"


class MCPrimitiveVar:
    def __init__(self, player: str, objective: str, function: "MCFunction", initial_value: int = None):
        # TODO: make sure objective is valid
        self.player = player
        self.objective = objective
        self.set_function(function)
        if initial_value is not None:
            self.set(initial_value)

    def set(self, value: int):
        # TODO: assert self.function != None
        self.function.add_command(mccw.score_set_cons(self.player, self.objective, value), f"{self} = {value}")

    def add(self, value: int):
        self.function.add_command(mccw.score_add_const(self.player, self.objective, value), f"{self} += {value}")

    def __str__(self):
        return f"{self.player}@{self.objective}"

    def print(self):
        # TODO: Create tellraw generator library
        self.function.add_command(mccw.print_score(self.player, self.objective), f"print({self})")

    def set_function(self, function: "MCFunction"):
        self.function = function
        self.function.add_objective(self.objective)


class MCClass:
    def __init__(self):
        self.functions: list["MCFunction"] = []


from mctpyes import *


class Namespace:
    def __init__(self):
        self.functions: list[MCFunction] = []

    def add_function(self, function: "MCFunction"):
        self.functions.append(function)

    def get_code(self) -> Code:
        return sum([function.get_function_list() for function in self.functions], [])

    def get_objectives(self):
        return sum([function.objectives for function in self.functions], [])

    def get_install(self, name: str = "__install__") -> Code:
        return [f"### {name}"] + [mccw.add_scoreboard_objective(objective) for objective in self.get_objectives()]


class MCFunction:
    def __init__(self, name: str, arguments: tuple["str"] = ()):
        self.commands: Code = []
        self.name = name
        self.arguments = ()
        self.objectives = []
        for argument in arguments:
            var = self.get_var(argument, scope=self)

            # pop
            self.comment(f"pop {var}")
            self.call_function("pop")

            # define var
            self.add_command(mccw.score_set(var.player, var.objective, "ret", "mcutils"), "finish pop")

            # add var to arg list
            self.arguments += (var,)

    def get_arg_vars(self):
        return self.arguments

    def comment(self, comment: str):
        self.commands.append(f"# {comment}")

    def add_objective(self, objective: str):
        assert len(objective) <= 16
        self.objectives.append(objective)

    def call_function(self, function: Union["MCFunction", str], arguments: tuple[MCPrimitiveVar] = ()):
        # TODO: maybe implement library requirement system
        # push arguments to stack
        # reverse arguments because first arguments are pushed first so the last argument is the first to be popped
        arguments = list(arguments)
        arguments.reverse()

        for argument in arguments:
            self.add_command(mccw.score_set("arg", "mcutils", argument.player, argument.objective),
                             f"set arg {argument} for mcutils push operation")
            self.add_command(mccw.call_function("$push"), "invoke mcutils push operation")
        if isinstance(function, MCFunction):
            name = function.name
        else:
            name = function
            # TODO: Another warning here
            print(f"Try using an MCFunction object instead of a str: {function}")

        self.add_command(mccw.call_function(f"${name}"), f"call {name} function")

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

    def get_var(self, name: str, scope: Union[Namespace, "MCFunction", str] = None, initial_value: int = None):
        scope = self if scope is None else scope

        if scope == "self":
            player = "@e[tag=mcutils.ret, limit=1]"
        elif isinstance(scope, str):
            player = scope
        else:
            player = scope.get_player()

        return MCPrimitiveVar(player, name, self, initial_value)

    def create_object(self, mcclass: MCClass):
        # calls create_object backend function
        # self.call_mc
        raise NotImplementedError

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
