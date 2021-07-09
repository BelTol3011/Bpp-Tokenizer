from typing import Literal

from ..classes import *

# both's functions are None on purpose since they shouldn't be changed
argument_var = MCPrimitiveVar("arg", "mcutils", None)
return_var = MCPrimitiveVar("ret", "mcutils", None)
return_selector = "@e[tag=mcutils.ret, limit=1]"

load = MCFunction("load")
create_object = MCFunction("create_object")
fetch_object = MCFunction("fetch_object")
push = MCFunction("push")
pop = MCFunction("pop")

NoneType = type(None)
_arguments = {load: NoneType,
              create_object: NoneType,
              fetch_object: MCPrimitiveVar,
              push: MCPrimitiveVar,
              pop: NoneType}


def call_function(command_acceptor: MCFunction,
                  function: MCFunction,
                  arg: MCPrimitiveVar = None) -> Union[MCPrimitiveVar, None]:
    expected_type = _arguments[function]
    # noinspection PyTypeHints
    compile_assert(isinstance(arg, expected_type), f"libmcutils.{function.name}: invalid argument: expected type "
                                                   f"{expected_type}, got {arg}")

    command_acceptor.comment(f"libmcuils: {function.name}({arg if arg else ''})")

    # set args
    if arg:
        command_acceptor.comment(f"setting arg")
        command_acceptor.score_copy(argument_var, arg)

    command_acceptor.call_function(function, comment="call the actual function")

    return return_var
