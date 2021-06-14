from typing import Literal

from ..classes import *

# both's functions are None on purpose since they shouldn't be changed
argument_var = MCPrimitiveVar("arg", "mcutils", None)
return_var = MCPrimitiveVar("ret", "mcutils", None)
return_selector = "@e[tag=mcutils.ret, limit=1]"


def call_function(command_acceptor: MCFunction,
                  function_name: Literal["load", "create_object", "fetch_object", "push", "pop"],
                  arg: MCPrimitiveVar = None) -> MCPrimitiveVar:
    # set args
    if arg:
        command_acceptor.score_copy(argument_var, arg)

    command_acceptor.call_function(function_name)

    return return_var
