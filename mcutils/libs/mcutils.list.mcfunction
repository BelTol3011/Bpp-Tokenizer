### load
say Loading libmcutils v2 module...

#?debug
say 0: Adding scores
scoreboard objectives add mcutils dummy
scoreboard objectives add mcutils.index dummy
scoreboard objectives add mcutils.obj_id dummy
scoreboard objectives add mcutils.value dummy

#?debug
say 1: Resetting scores
scoreboard players set latest_id mcutils 0
scoreboard players set stack_len mcutils 0

#?debug
say 2: Removing all previous objects
kill @e[tag=mcutils.object]
kill @e[tag=mcutils.stack]

tag @e remove mcutils.ret
tag @e remove mcutils.object
tag @e remove mcutils.stack

say Everything finished!

### create_object
# ensure no entities have the temp tag
tag @e remove mcutils.temp

# summon entity
summon armor_stand 0 64 0 {Tags: ["mcutils.object", "mcutils.temp"]}

# store obj_id
scoreboard players operation @e[tag=mcutils.temp, limit=1] mcutils.obj_id = latest_id mcutils

# return obj_id
scoreboard players operation ret mcutils = latest_id mcutils

# increment latest_id
scoreboard players add latest_id mcutils 1

### fetch_object
tag @e remove mcutils.ret
execute as @e if score @s mcutils.obj_id = arg mcutils run tag @s add mcutils.ret

### push
# increment stack_len by 1
scoreboard players add stack_len mcutils 1

# ensure no entities have the temp tag
tag @e remove mcutils.temp

# summon entity
summon armor_stand 0 64 0 {Tags: ["mcutils.stack", "mcutils.temp"]}

# assign scores
scoreboard players operation @e[tag=mcutils.temp, limit=1] mcutils.index = stack_len mcutils
scoreboard players operation @e[tag=mcutils.temp, limit=1] mcutils.value = arg mcutils

### pop
# ensure no entities have the temp tag
tag @e remove mcutils.temp

# find entity
execute as @e if score @s mcutils.index = stack_len mcutils run tag @s add mcutils.temp

# read score
scoreboard players operation ret mcutils = @e[tag=mcutils.temp, limit=1] mcutils.value

# kill entity
kill @e[tag=mcutils.temp]

# decrement stack_len by 1
scoreboard players remove stack_len mcutils 1