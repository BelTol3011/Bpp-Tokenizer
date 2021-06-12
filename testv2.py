from minecraft_utils_v2 import *
import deployment_engine as de

c = Namespace(namespace="testest")
# TODO: create Namespace.get_var_name()

test_function = MCFunction("test", ("testarg", ))
arg, = test_function.get_arg_vars()
test_function.say("In function now")
arg.print()

main = MCFunction("tick")
main.say("tick")
# TODO: main.get_var("e")
e = MCPrimitiveVar("tick", "e", main)
e.add(1)
e.print()
main.call_function(test_function, (e, ))

# DEPLOYMENT
c.add_function(main)
c.add_function(test_function)

print(c.get_code())
with open("libs/mcutils.list.mcfunction", "r") as f:
    libmcutils_code = f.read().split("\n")
print(c.get_code())
de.to_datapack([(de.Path(("main", [])), c.get_code()+c.get_install()),
                (de.Path(("mcutils", [])), libmcutils_code)],
               "Datapack",
               {"debug"})
# print(pp_code(c.get_code()))
