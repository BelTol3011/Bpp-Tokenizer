from minecraft_utils_v2 import MCPrimitiveVar

# both's functions are None on purpose since they shouldn't be changed
argument_var = MCPrimitiveVar("arg", "mcutils", None)
return_var = MCPrimitiveVar("ret", "mcutils", None)
return_selector = "@e[tag=mcutils.ret, limit=1]"

load = "load"
create_object = "create_object"
fetch_object = "fetch_object"
push = "push"
pop = "pop"
