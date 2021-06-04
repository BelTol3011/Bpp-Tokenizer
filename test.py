from minecraft_utils import *

set_minecraft_namespace("testest")

a, b, c, d, e = vars("a b c d e")

step_in("tick")
print_str("tick")
add_int(e, 1)
print_variable(e)
step_out()

set_value(a, 10)
copy(a, b)
while_loop_start(b)

set_value(c, 10)
while_loop_start(c)

print_variable(c)
sub_int(c, 1)
copy(c, d)
sub_int(d, 5)
if_start(d)

print_str("iflol")

if_end()

while_loop_end()

print_variable(b)
sub_int(b, 1)

while_loop_end()

EXPORT()
GET()
print(EXPORT(path="."))
