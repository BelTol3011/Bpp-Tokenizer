from . import *
from . import mcjson
from . import mc_command_wrapper as mccw

from typing import Union
import sys
from typing import Iterable
import warnings
import traceback

Code = list[str]
META_OBJECTIVE = "__mcutils__"
RETURN_PLAYER = "ret"


class MCPrimitiveVar:
    def __init__(self, player: str, objective: str, function: Union["MCFunction", None], initial_value: int = None):
        # TODO: make sure objective is valid
        self.player = player
        self.objective = objective
        self.set_function(function)
        if initial_value is not None:
            self.set(initial_value)

    def set(self, value: int):
        # TODO: assert self.function != None
        self.function.add_command(mccw.score_set_const(self.player, self.objective, value), f"{self} = {value}")

    def add(self, value: int):
        self.function.add_command(mccw.score_add_const(self.player, self.objective, value), f"{self} += {value}")

    def __str__(self):
        return f"{self.objective}@{self.player}"

    def print(self, player: str = "@a"):
        self.function.tellraw(
            player,
            mcjson.get_raw_json(mcjson.ScoreboardValue(player=self.player, objective=self.objective)),
            f"print({self})"
        )

    def set_function(self, function: "MCFunction"):
        self.function = function
        # TODO: deal with NoneType functions
        if self.function:
            self.function.add_objective(self.objective)

    def call_function(self, function: "MCFunction", args: tuple["MCPrimitiveVar"]):
        # TODO: if context is already set, no need to set it again
        # TODO: change context back after calling the function
        # change context to this object via fetch_object
        self.function.comment(f"{self}.{function}({pp_args(args)})")
        self.function.comment("Set args for fetch_object")
        self.function.score_copy(libmcutils.argument_var, self)
        self.function.call_function(libmcutils.fetch_object)

        # call the function
        self.function.call_function(function, args)


class MCClass:
    def __init__(self, name: str):
        self.functions: list["MCFunction"] = []
        # TODO: deal with empty init functions
        self.init = None
        self.name = name

    def create_function(self, name: str, args: tuple[str] = (), is_init: bool = False) -> "MCFunction":
        function = MCFunction(f"{name}_{self.name}", args, libmcutils.return_selector)

        self.functions.append(function)
        if is_init:
            self.init = function
        return function

    def get_init(self):
        return self.init


class MCNamespace:
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


class CompilationWarning(Warning):
    def __init__(self, message: str, command: str):
        super().__init__(f"{message}: {command}")


class MCFunction:
    def __init__(self, name: str, arguments: tuple[str] = (), player: str = None):
        self.commands: Code = []
        self.name = name
        self.arguments: tuple[MCPrimitiveVar] = ()
        self.objectives = []
        self.player = player
        for argument in arguments:
            var = self.get_var(argument, scope=self)

            # pop
            self.comment(f"pop {var}")
            self.call_function("pop")

            # define var
            # TODO: Change to libmcutils library
            self.add_command(mccw.score_set(var.player, var.objective, "ret", "mcutils"), "finish pop")

            # add var to arg list
            self.arguments += (var,)

    def __str__(self):
        return self.name

    def get_arg_vars(self):
        return self.arguments

    def comment(self, comment: str):
        self.commands.append(f"# {comment}")

    def add_objective(self, objective: str):
        assert len(objective) <= 16
        self.objectives.append(objective)

    def call_function(self, function: Union["MCFunction", str], arguments: tuple[MCPrimitiveVar] = ()):
        self.comment(f"{function}({pp_args(arguments)})")
        # TODO: maybe implement library requirement system
        # push arguments to stack
        # reverse arguments because first argument is pushed first so the last argument is the first to be popped
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
            issue_warning(CompilationWarning("Try using an MCFunction object instead of a str", function))

        self.add_command(mccw.call_function(f"${name}"), f"call {name} function")

    def get_function_list(self) -> Code:
        return [f"### {self.name}"] + self.commands

    def get_player(self):
        # mcfunctions are static so this is constant
        return self.player or f"{self.name}_func"

    def get_code(self):
        return self.commands

    def return_(self, var: Union[MCPrimitiveVar]):
        # set return score
        self.add_command(mccw.score_set(RETURN_PLAYER, META_OBJECTIVE, var.player, var.objective), f"return {var}")

    def get_var(self, name: str, scope: Union[MCNamespace, "MCFunction", str] = None, initial_value: int = None):
        scope = self if scope is None else scope

        if scope == "self":
            player = "@e[tag=mcutils.ret, limit=1]"
        elif isinstance(scope, str):
            player = scope
        else:
            player = scope.get_player()

        return MCPrimitiveVar(player, name, self, initial_value)

    def create_object(self, class_: MCClass, name: str, args: tuple[MCPrimitiveVar]) -> MCPrimitiveVar:
        # call create_object backend
        self.call_function("create_object")

        # create the variable with the object id
        var = self.get_var(name)
        self.score_copy(var, libmcutils.return_var)

        # call init of object
        var.call_function(class_.get_init(), args)

        return var

    def add_command(self, command: str, comment: str = ""):
        """Appends the minecraft command specified to the command list"""
        if comment:
            self.commands.append(f"# {comment}")
        else:
            issue_warning(CompilationWarning("No comment provided", command))
            self.commands.append(f"# {command}")
        self.commands.append(command)
        self.commands.append("")
        # self.commands.append('execute if entity @e[tag=mcutils.stack] run say Stack!:')
        # self.commands.append('execute if entity @e[tag=mcutils.stack] as @e[tag=mcutils.stack] run tellraw @a [{"score": {"name": "@e[tag=mcutils.stack]", "objective": "mcutils.value"}}]')

    def add_commands(self, commands: list[str]):
        """Appends a list of commands and premises to the command list"""
        # TODO: make comments able to be disabled
        for command in commands:
            if command is None:
                continue
            self.add_command(command)

    def say(self, message: str, comment: str = ""):
        self.add_command((command := mccw.say(message)), comment or command)

    def tellraw(self, player: str, raw_json: str, comment: str = ""):
        self.add_command(mccw.tellraw(player, raw_json), comment)

    def score_copy(self, target_var: MCPrimitiveVar, origin_var: MCPrimitiveVar):
        self.add_command(
            mccw.score_set(target_var.player, target_var.objective, origin_var.player, origin_var.objective),
            f"{target_var} = {origin_var}")


def issue_warning(warning: Warning):
    warnings.warn(warning)
    sys.stderr.write("".join(traceback.format_stack()[:-1]) + "\n")


def pp_args(args: Iterable[MCPrimitiveVar], sep: str = ", "):
    return sep.join([str(arg) for arg in args])


from .libs import libmcutils
