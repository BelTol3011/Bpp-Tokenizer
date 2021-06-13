from minecraft_utils_v2 import *
import deployment_engine as de

n = Namespace()

object_test = MCFunction("object_test")

# TODO: differentiate between object and function scope, might be impossible though
#  since scopes are determined at compile time

myclass = MCClass("dog")
dog_init = myclass.create_function("dog_init", ("number",), is_init=True)
number, = dog_init.get_arg_vars()
dog_init.say("INIT")
number.print()
dog_nr_var = dog_init.get_var("number")
dog_init.score_copy(dog_nr_var, number)

dog_bark = myclass.create_function("bark", ("message",))
message, = dog_bark.get_arg_vars()
dog_bark.say("BARKBARK")
number = dog_bark.get_var("number")
message.print()

mydog1 = object_test.create_object(myclass, "mydog", (object_test.get_var("test", initial_value=1), ))
mydog3 = object_test.create_object(myclass, "mydog3", (object_test.get_var("test", initial_value=3), ))

mydog1.call_function(dog_bark, (object_test.get_var("test", initial_value=15), ))
mydog3.call_function(dog_bark, (object_test.get_var("test", initial_value=35), ))

# DEPLOYMENT
n.add_function(object_test)
n.add_function(dog_init)
n.add_function(dog_bark)
print(n.get_code())
with open("libs/mcutils.list.mcfunction", "r") as f:
    libmcutils_code = f.read().split("\n")
print(n.get_code())
de.to_datapack([(de.Path(("unittest", [])), n.get_code() + n.get_install()),
                (de.Path(("mcutils", [])), libmcutils_code)],
               "Datapack",
               {"debug"})
