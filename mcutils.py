from minecraft_utils_v2 import *
from mc_command_wrapper import *


# !!!!!!!!! UNFINISHED !!!!!!!!!!
# attempt of creating a "dynamic" version of the
# libmcutils library as in libs/libmcutils.list.mcfunction


def get_functions(premises: set[str]) -> list[MCFunction]:
    load = MCFunction("load")
    load.add_commands([say("Loading libmcutils v2 module..."),

                       say("0: Adding scores") if "debug" in premises else None,
                       add_scoreboard_objective("mcutils"),
                       add_scoreboard_objective("mcutils.index"),
                       add_scoreboard_objective("mcutils.obj_id"),
                       add_scoreboard_objective("mcutils.value"),

                       say("1: Resetting scores") if "debug" in premises else None,
                       score_set_cons("latest_id", "mcutils", 0),
                       score_set_cons("stack_len", "mcutils", 0),

                       say("2: Removing all previous objects") if "debug" in premises else None,
                       kill("@e[tag=mcutils.object]"),
                       kill("@e[tag=mcutils.stack]"),
                       ])
    # TODO: finish this
    create_object = MCFunction("create_object")
    fetch_object = MCFunction("fetch_object")
    push = MCFunction("push")
    pop = MCFunction("pop")
    return [load, create_object, fetch_object, push, pop]
