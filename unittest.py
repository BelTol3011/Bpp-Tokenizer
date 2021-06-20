from mcutils import *
from mcutils import deployment_engine as de

n = MCNamespace()

object_test = MCFunction("object_test", (), n)

# TODO: differentiate between object scope (self) and object-function-local scope, might be impossible though
#  since scopes are determined at compile time. This causes pop operations to be directly saved into the object rather
#  that discarded after the return of a function


myclass = MCClass("dog")
dog_init = myclass.create_function("init", ("number",), is_init=True)
number, = dog_init.get_arg_vars()
dog_init.say("running init, number is:")
number.print()
dog_nr_var = dog_init.get_var("number")
dog_init.score_copy(dog_nr_var, number)
dog_init.say("end init")

dog_bark = myclass.create_function("bark", ("message",))
message, = dog_bark.get_arg_vars()
dog_bark.say("Running bark, arg is:")
number = dog_bark.get_var("number")
message.print()
dog_bark.say("number is:")
number.print()
dog_bark.say("end bark")

mydog1 = object_test.create_object(myclass, "mydog", (object_test.get_var("test", initial_value=1), ))
mydog3 = object_test.create_object(myclass, "mydog3", (object_test.get_var("test", initial_value=3), ))

mydog1.call_function(dog_bark, (object_test.get_var("test", initial_value=15), ))
mydog3.call_function(dog_bark, (object_test.get_var("test", initial_value=35), ))

# DEPLOYMENT
object_test.set_namespace(n)
dog_init.set_namespace(n)
dog_bark.set_namespace(n)
print(n.get_code())
with open("mcutils/libs/mcutils.list.mcfunction", "r") as f:
    libmcutils_code = f.read().split("\n")
print(n.get_code())
de.to_datapack([(de.Path(("unittest", [])), n.get_code() + n.get_install()),
                (de.Path(("mcutils", [])), libmcutils_code)],
               "Datapack",
               {"debug"})
