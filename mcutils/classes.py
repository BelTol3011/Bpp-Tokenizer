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
        # change context to this object via fetch_object
        self.function.comment(f"{self}.{function}({pp_args(args)})")

        libmcutils.call_function(self.function, libmcutils.fetch_object, self)

        # call the function as the fetched object
        self.function.call_function(function, args, player=libmcutils.return_selector,
                                    comment="call the function as the fetched object")


class MCClass:
    def __init__(self, name: str):
        self.functions: list["MCFunction"] = []
        # TODO: deal with empty init functions
        self.init = None
        self.name = name

    def create_function(self, name: str, args: tuple[str] = (), is_init: bool = False) -> "MCFunction":
        # TODO: add namespace argument
        function = MCFunction(f"{self.name}_{name}", args, player="@s")

        self.functions.append(function)
        if is_init:
            self.init = function
        return function

    # TODO: consider calling a __create__ function instead of baking it hard code into the function on step above on
    #  object creation. Maybe add support for hard linking ("$oo" instead of "function $foo")?

    def get_init(self):
        return self.init


class MCNamespace:
    def __init__(self):
        self.functions: set[MCFunction] = set()
        self.function_names: dict[str: int] = {}

    def add_function(self, function: "MCFunction"):
        self.functions.add(function)

    def get_code(self) -> Code:
        return sum([function.get_function_list() for function in self.functions], [])

    def get_objectives(self):
        return sum([function.objectives for function in self.functions], [])

    def get_install(self, name: str = "__install__") -> Code:
        return [f"### {name}"] + [mccw.add_scoreboard_objective(objective) for objective in self.get_objectives()]

    def get_function_name(self, name):
        """returns a unique function name beginning with `name`."""
        if name not in self.function_names:
            self.function_names.update({name: 0})
        else:
            self.function_names[name] += 1

        return name + str(self.function_names[name])


class MCFunction:
    def __init__(self, name: str, arguments: tuple[str, ...] = (), namespace: MCNamespace = None, player: str = None):
        self.commands: Code = []
        self.sub_functions: list[MCFunction] = []
        self.name = name
        self.arguments: tuple[MCPrimitiveVar, ...] = ()
        self.objectives = []
        self.player = player
        self.namespace: MCNamespace = namespace

        if namespace:
            self.namespace.add_function(self)

        for argument in arguments:
            var = self.get_var(argument, scope=self)

            # pop
            self.comment(f"pop {var}")
            result = libmcutils.call_function(self, libmcutils.pop)

            # define var
            self.score_copy(var, result)

            # add var to arg list
            self.arguments += (var,)

    def __str__(self):
        return self.name

    def set_namespace(self, namespace: MCNamespace):
        self.namespace = namespace
        self.namespace.add_function(self)

    def get_arg_vars(self):
        return self.arguments

    def comment(self, comment: str):
        self.commands.append(f"# {comment}")

    def add_objective(self, objective: str):
        assert len(objective) <= 16
        self.objectives.append(objective)

    def call_function(self, function: Union["MCFunction", str], arguments: tuple[MCPrimitiveVar] = (),
                      player: str = None, comment: str = ""):
        # push arguments to stack
        # reverse arguments because first argument is pushed first so the last argument is the first to be popped
        arguments = list(arguments)
        arguments.reverse()

        for argument in arguments:
            libmcutils.call_function(self, libmcutils.push, argument)

        if isinstance(function, MCFunction):
            name = function.name
        else:
            name = function
            issue_warning(CompilationWarning("Try using an MCFunction object instead of a str", function))

        command = mccw.call_function(f"${name}")  # , f"call {name} function"
        if player:
            command = Execute().as_(player).at("@s").run(command)
        self.add_command(command, comment=comment)

        self.comment(f"{function}({pp_args(arguments)})")

    def get_function_list(self) -> Code:
        return [f"### {self.name}", f"# args: {pp_args(self.arguments)}"] + self.get_code() + \
               sum([function.get_function_list() for function in self.sub_functions], [])

    def get_player(self):
        # mcfunctions are static so this is constant
        return self.player or f"{self.name}_func"

    def get_code(self):
        return self.commands

    def return_(self, var: Union[MCPrimitiveVar]):
        # set return score
        # TODO: make this consistent
        self.add_command(mccw.score_set(RETURN_PLAYER, META_OBJECTIVE, var.player, var.objective), f"return {var}")

    def get_var(self, name: str, scope: Union[MCNamespace, "MCFunction", str] = None, initial_value: int = None):
        scope = self if scope is None else scope

        if scope == "self":
            player = "@s"
        elif isinstance(scope, str):
            player = scope
        else:
            player = scope.get_player()

        return MCPrimitiveVar(player, name, self, initial_value)

    def create_object(self, class_: MCClass, name: str, args: tuple[MCPrimitiveVar]) -> MCPrimitiveVar:
        # call create_object backend
        object_id = libmcutils.call_function(self, libmcutils.create_object)

        # create the variable with the object id
        var = self.get_var(name)
        self.score_copy(var, object_id)

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

    def execute(self, execute: "Execute") -> "MCFunction":
        assert self.namespace is not None, \
            "Can't create an execute function without namespace because of function name collision risk!"

        new_function = MCFunction(f"{self.name}_{self.namespace.get_function_name('execute')}",
                                  namespace=self.namespace)
        self.sub_functions.append(new_function)

        # call the execute
        self.add_command(execute.run(mccw.call_function(f"${new_function.name}")), "Call execute function")

        return new_function

    def say(self, message: str, comment: str = ""):
        self.add_command((command := mccw.say(message)), comment or command)

    def tellraw(self, player: str, raw_json: str, comment: str = ""):
        self.add_command(mccw.tellraw(player, raw_json), comment)

    def score_copy(self, target_var: MCPrimitiveVar, origin_var: MCPrimitiveVar):
        self.add_command(
            mccw.score_set(target_var.player, target_var.objective, origin_var.player, origin_var.objective),
            f"{target_var} = {origin_var}")


def pp_args(args: Iterable[MCPrimitiveVar], sep: str = ", "):
    return sep.join([str(arg) for arg in args])


from .libs import libmcutils
from .mcexecute import Execute
