from minecraft_utils_v2 import *
import deployment_engine as de

c = Namespace(namespace="testest")

arg = MCPrimitiveVar("test", "testarg")
test_function = c.create_function("test", arg)
test_function.say("In function now")
arg.print()

main = c.create_function("tick")
main.say("tick")
e = MCPrimitiveVar("tick", "e", main)
e.add(1)
e.print()
main.call_function(test_function, e)

# DEPLOYMENT
print(c.get_code())
with open("libs/mcutils.list.mcfunction", "r") as f:
    libmcutils_code = f.read().split("\n")
de.to_datapack([(de.Path(("main", [])), c.get_code()),
                (de.Path(("mcutils", [])), libmcutils_code)],
               "Datapack",
               {"debug"})
# print(pp_code(c.get_code()))
