# TODO: create some kind of wrapper for @e, @a, @p, etc..

def say(message: str):
    return f"say {message}"


def call_function(name: str):
    return f"function {name}"


def add_scoreboard_objective(name: str, criteria: str = "dummy", display_name: str = ""):
    # TODO: check if criteria is valid
    # TODO: check if display name is valid

    assert len(name) <= 16, "Scoreboard objectives mustn't be longer than 16 chars."

    return f"scoreboard objectives add {name} {criteria} {display_name}".rstrip()


def print_score(player: str, objective: str, target: str = "@a"):
    assert len(objective) <= 16, "Scoreboard objectives mustn't be longer than 16 chars."

    return f'tellraw {target} {{"score":{{"name":"{player}","objective":"{objective}"}}}}'


def kill(entity: str):
    return f"kill {entity}"


def tellraw(player: str, raw_json: str):
    return f"tellraw {player} {raw_json}"


def score_set_const(player: str, objective: str, value: int):
    return f"scoreboard players set {player} {objective} {value}"


def score_set(target_player: str, target_objective: str, origin_player: str, origin_objective: str):
    return f"scoreboard players operation {target_player} {target_objective} = {origin_player} {origin_objective}"


def score_add_const(player: str, objective: str, increment: int):
    return f"scoreboard players add {player} {objective} {increment}"
