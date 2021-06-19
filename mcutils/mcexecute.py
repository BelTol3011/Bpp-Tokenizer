# A python execute wrapper.
from typing import Literal
from .classes import MCPrimitiveVar


def execute_command(func):
    def wrapper(self, *args, **kwargs):
        self.string += f" {func(self, *args, **kwargs)}"

        return self

    return wrapper


def if_unless(func):
    def wrapper(self, if_unless: Literal["if", "unless"] = "if", *args, **kwargs):
        return f"{if_unless} {func(self, *args, **kwargs)}"

    return wrapper


def result_success(func):
    def wrapper(self, result_success: Literal["result", "success"] = "result", *args, **kwargs):
        return f"store {result_success} {func(self, *args, **kwargs)}"

    return wrapper


class Execute:
    def __init__(self):
        self.string = "execute"

    def __str__(self):
        return self.string

    @execute_command
    def align(self, align_x: bool = False, align_y: bool = False, align_z: bool = False):
        assert align_x or align_y or align_z, "At least on must be True"

        return f"align {align_x * 'x'}{align_y * 'y'}{align_z * 'z'}"

    @execute_command
    def anchored(self, anchor: Literal["eyes", "feet"]):
        return f"anchored {anchor}"

    @execute_command
    def as_(self, targets: str):
        return f"as {targets}"

    @execute_command
    def at(self, targets: str):
        return f"at {targets}"

    @execute_command
    def facing_position(self, position: str):
        return f"facing {position}"

    @execute_command
    def facing_entity(self, targets: str, anchor: Literal["eyes", "feet"]):
        return f"facing entity {targets} {anchor}"

    @execute_command
    def in_(self, dimension: Literal["overworld", "the_nether", "the_end"]):
        return f"in {dimension}"

    @execute_command
    def positioned_absolute(self, position: str):
        return f"positioned {position}"

    @execute_command
    def positioned_as(self, targets: str):
        return f"positioned as {targets}"

    @execute_command
    def rotated_absolute(self, rotation: str):
        return f"rotated {rotation}"

    @execute_command
    def rotated_as(self, targets: str):
        return f"rotated as {targets}"

    @execute_command
    @if_unless
    def if_block(self, position: str, block: str):
        return f"block {position} {block}"

    @execute_command
    @if_unless
    def if_blocks(self, start_pos: str, end_pos: str, destination_pos: str, scan_mode: Literal["all", "masked"]):
        return f"blocks {start_pos} {end_pos} {destination_pos} {scan_mode}"

    @execute_command
    @if_unless
    def if_data_block(self, position: str, path: str):
        return f"data block {position} {path}"

    @execute_command
    @if_unless
    def if_data_entity(self, target: str, path: str):
        return f"data entity {target} {path}"

    @execute_command
    @if_unless
    def if_data_storage(self, source: str, path: str):
        return f"data storage {source} {path}"

    @execute_command
    @if_unless
    def if_entity(self, targets: str):
        return f"entity {targets}"

    @execute_command
    @if_unless
    def if_predicate(self, predicate: str):
        return f"predicate {predicate}"

    @execute_command
    @if_unless
    def if_score_compare(self, target: MCPrimitiveVar, operation: Literal["<", "<=", "=", ">=", ">"],
                         source: MCPrimitiveVar):
        return f"score {target.player} {target.objective} {operation} {source.player} {source.objective}"

    @execute_command
    @if_unless
    def if_score_matches(self, target: MCPrimitiveVar, range_: str):
        return f"score {target.player} {target.objective} matches {range_}"

    @execute_command
    @result_success
    def store_block(self, target_pos: str, path: str, type_: Literal["byte", "short", "int", "Long", "float", "double"],
                    scale: float = 1.0):
        return f"block {target_pos} {path} {type_} {scale}"

    @execute_command
    @result_success
    def store_bossbar(self, id_: str, value: Literal["value", "max"]):
        return f"bossbar {id_} {value}"

    @execute_command
    @result_success
    def store_entity(self, target: str, path: str, type_: Literal["byte", "short", "int", "Long", "float", "double"],
                     scale: float = 1.0):
        return f"entity {target} {path} {type_} {scale}"

    @execute_command
    @result_success
    def store_score(self, target: MCPrimitiveVar):
        return f"score {target.player} {target.objective}"

    @execute_command
    @result_success
    def store_storage(self, target: str, path: str, type_: Literal["byte", "short", "int", "Long", "float", "double"],
                      scale: float = 1.0):
        return f"storage {target} {path} {type_} {scale}"

    @execute_command
    def run(self, command: str):
        return f"run {command}"
