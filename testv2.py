from minecraft_utils_v2 import *
import deployment_engine as de

c = Namespace(namespace="testest")
main = c.create_function("tick")
main.say("tick")
e = main.get_var("e", main)
e.add(1)
e.print()



print(c.get_code())
de.to_datapack([(de.Path(("main", [])), c.get_code())],
               "Datapack",
               {"debug"})
# print(pp_code(c.get_code()))
