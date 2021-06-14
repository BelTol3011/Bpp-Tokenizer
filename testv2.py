from mcutils import *
from mcutils import deployment_engine as de

c = Namespace()
# TODO: create Namespace.get_var_name()

test_function = MCFunction("test", ("testarg", ))
arg, = test_function.get_arg_vars()
test_function.say("In function now")
arg.print()

main = MCFunction("tick")
main.say("tick")
e = main.get_var("e")
e.add(1)
e.print()
main.call_function(test_function, (e, ))


# DEPLOYMENT
c.add_function(main)
c.add_function(test_function)


with open("mcutils/libs/mcutils.list.mcfunction", "r") as f:
    libmcutils_code = f.read().split("\n")
de.to_datapack([(de.Path(("main", [])), c.get_code()+c.get_install()),
                (de.Path(("mcutils", [])), libmcutils_code)],
               "Datapack",
               {"debug"})
# print(pp_code(c.get_code()))
