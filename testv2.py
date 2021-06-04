from minecraft_utils_v2 import *

c = MCCompiler(namespace="testest")
main = MCMain(c)

tick = MCFunction("tick", main)
tick.print_str("tick")
tick.uint_add_constint(e, 1)

print(pp_code(c.get_code()))
