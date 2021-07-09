import json
from typing import Literal, Union

VALID_COLORS = ["black", "dark_blue", "dark_green", "dark_aqua", "dark_red", "dark_purple", "gold", "gray", "dark_gray",
                "blue", "green", "aqua", "red", "light_purple", "yellow", "white", "reset"]

NOT_SPECIFIED = type("NotSpecified", (), {})


# TODO: be able to use str type instead of only TextComponent

class ClickEvent:
    def __init__(self,
                 action: Literal["open_url",
                                 "open_file",
                                 "run_command",
                                 "suggest_command",
                                 "change_page",
                                 "copy_to_clipboard"],
                 value: Union[str, int]):
        self.action = action
        self.value = value

    def get_dict(self) -> dict:
        return {"action": self.action, "value": self.value}


class HoverEvent:
    def get_action(self):
        raise NotImplementedError

    def get_contents(self):
        raise NotImplementedError

    def get_dict(self) -> dict:
        return {"action": self.get_action(),
                "contents": self.get_contents()}


class ShowText(HoverEvent):
    def __init__(self, text_components: list["TextComponent"]):
        self.text_components = text_components

    def get_action(self):
        return "show_text"

    def get_contents(self):
        return get_raw_dict(*self.text_components)


class ShowItem(HoverEvent):
    def __init__(self, item_snbt: dict):
        # TODO: implement item wrapper
        self.item_snbt = item_snbt

    def get_action(self):
        return "show_item"

    def get_contents(self):
        return self.item_snbt


class ShowEntity(HoverEvent):
    def __init__(self, entity_type: str, entity_id: str, name: "TextComponent" = NOT_SPECIFIED):
        """
        :param entity_type: A string containing the namespaced entity ID.
        :param entity_id: A string containing the UUID of the entity in hyphenated hexadecimal format.
        :param name: The TextComponent to be displayed as the name of the Entity.
        HoverEvent hidden if left not specified.
        """
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.name = name
        raise Exception("Somehow, this is defunct, take a look at https://bugs.mojang.com/browse/MC-76246. "
                        "Comment this line if you want to try it anyway.")

    def get_action(self):
        return "show_entity"

    def get_contents(self):
        return {"name": self.name, "type": self.entity_type, "id": self.entity_id}


class TextComponent:
    def __init__(self,
                 color: str = NOT_SPECIFIED,
                 font: str = NOT_SPECIFIED,
                 bold: bool = NOT_SPECIFIED,
                 italic: bool = NOT_SPECIFIED,
                 underlined: bool = NOT_SPECIFIED,
                 strikethrough: bool = NOT_SPECIFIED,
                 obfuscated: bool = NOT_SPECIFIED,
                 insertion: str = NOT_SPECIFIED,
                 click_event: ClickEvent = NOT_SPECIFIED,
                 hover_event: HoverEvent = NOT_SPECIFIED,
                 extra: list["TextComponent"] = NOT_SPECIFIED):
        """
        :param color: The color to render the content in. Valid values are VALID_COLORS or #RRGGBB.
        :param font: The resource location of the font. Default is "minecraft: default".
        :param bold: Whether to render the content in bold.
        :param italic: Whether to render the content in italics.
        :param underlined: Whether to underline the content.
        :param strikethrough: Whether to strikethrough the content.
        :param obfuscated: Whether to render the content obfuscated.
        :param insertion: Insertion into their chat input when text is shift-clicked py a player.
        :param click_event: Event that is executed when the text is clicked in chat.
        :param hover_event: Allows for a tooltip to be displayed when the player hovers their mouse over text.
        :param extra: A list of additional TextComponents to be displayed after this one that inherit all formatting and
                      interactivity from this component unless overridden.
        """

        self.color = color
        self.font = font
        self.bold = bold
        self.italic = italic
        self.underlined = underlined
        self.strikethrough = strikethrough
        self.obfuscated = obfuscated
        self.insertion = insertion
        self.click_event = click_event
        self.hover_event = hover_event
        self.extra = extra

    def get_basic(self) -> dict:
        out = {"color": self.color if self.color != NOT_SPECIFIED else None,
               "font": self.font if self.font != NOT_SPECIFIED else None,
               "bold": self.bold if self.bold != NOT_SPECIFIED else None,
               "italic": self.italic if self.italic != NOT_SPECIFIED else None,
               "underlined": self.underlined if self.underlined != NOT_SPECIFIED else None,
               "strikethrough": self.strikethrough if self.strikethrough != NOT_SPECIFIED else None,
               "obfuscated": self.obfuscated if self.obfuscated != NOT_SPECIFIED else None,
               "insertion": self.insertion if self.insertion != NOT_SPECIFIED else None,
               "clickEvent": self.click_event.get_dict() if self.click_event != NOT_SPECIFIED else None,
               "hoverEvent": self.hover_event.get_dict() if self.hover_event != NOT_SPECIFIED else None}
        for key in list(out.keys()):
            if out[key] is None:
                del out[key]
        return out

    def get_special(self) -> dict:
        return {}

    def get_dict(self) -> dict:
        return self.get_basic() | self.get_special()


class PlainText(TextComponent):
    def __init__(self, text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text = text

    def get_special(self) -> dict:
        return {"text": self.text}


class TranslatedText(TextComponent):
    def __init__(self, translate: str, with_: list[TextComponent] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.translate = translate
        self.with_ = [] if with_ is None else with_

    def get_special(self) -> dict:
        return {"translate": self.translate, "with": get_raw_dict(*self.with_)}


class ScoreboardValue(TextComponent):
    def __init__(self, player: str, objective: str, *args, **kwargs):
        """
        :param player: may be "*" to list the scores of @a.
        """
        super().__init__(*args, **kwargs)

        self.player = player
        self.objective = objective

    def get_special(self) -> dict:
        return {"score": {"name": self.player, "objective": self.objective}}


class Selector(TextComponent):
    def __init__(self, player: str, separator: list[TextComponent] = NOT_SPECIFIED, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.player = player
        self.separator = separator

    def get_special(self) -> dict:
        return {"selector": self.player} | \
               ({"separator": get_raw_dict(*self.separator)} if self.separator != NOT_SPECIFIED else {})


class Keybind(TextComponent):
    def __init__(self, keybind: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.keybind = keybind

    def get_special(self) -> dict:
        return {"keybind": self.keybind}


class NBT(TextComponent):
    def __init__(self, path: str, interpret: bool = NOT_SPECIFIED, separator: list[TextComponent] = NOT_SPECIFIED,
                 block: str = NOT_SPECIFIED,
                 entity: str = NOT_SPECIFIED,
                 storage: str = NOT_SPECIFIED, *args, **kwargs):
        """
        :param path: The NBT path for looking up in block, entity or storage.
        :param interpret: If set to True, game attempts to parse the text as a TextComponent
        :param block: Coordinates of the block.
        :param entity: Selector.
        :param storage: Namespaced ID of the command storage.
        """
        super().__init__(*args, **kwargs)

        self.path = path
        self.interpret = interpret
        self.separator = separator
        self.block = block
        self.entity = entity
        self.storage = storage

        assert (block != NOT_SPECIFIED) or (entity != NOT_SPECIFIED) or (storage != NOT_SPECIFIED), \
            "at least one of block, entity and storage has to be set"

    def get_special(self) -> dict:
        return {"nbt": self.path} | \
               ({"interpret": self.interpret} if self.interpret != NOT_SPECIFIED else {}) | \
               ({"separator": get_raw_dict(*self.separator)} if self.separator != NOT_SPECIFIED else {}) | \
               ({"block": self.block} if self.block != NOT_SPECIFIED else {}) | \
               ({"entity": self.entity} if self.entity != NOT_SPECIFIED else {}) | \
               ({"storage": self.storage} if self.storage != NOT_SPECIFIED else {})


def get_raw_dict(*text_components: TextComponent) -> list:
    return [text_component.get_dict() for text_component in text_components]


def get_raw_json(*text_components: TextComponent) -> str:
    return json.dumps(get_raw_dict(*text_components))


def main():
    base_format_test = [PlainText("Tellraw Test:"), PlainText("Bold", bold=True), PlainText("Italic ", italic=True),
                        PlainText("Underlined ", underlined=True), PlainText("Strikethrough ", strikethrough=True),
                        PlainText("Obfuscated ", obfuscated=True),
                        *[PlainText(color, color=color) for color in VALID_COLORS]]
    print(get_raw_json(*base_format_test,
                       PlainText("Insertion ", insertion="insertion goes here"),
                       PlainText("ClickEventOpenURL ",
                                 click_event=ClickEvent("open_url", "https://example.org/")),
                       PlainText("ClickEventRunCommand ",
                                 click_event=ClickEvent("run_command", "/say WORKS!")),
                       PlainText("ClickEventSuggestCommand ",
                                 click_event=ClickEvent("suggest_command", "/say WOOP WOOP!")),
                       PlainText("ClickEventCopyClipboard ",
                                 click_event=ClickEvent("copy_to_clipboard", "clipboard goes here")),
                       PlainText("HoverEventShowText ", hover_event=ShowText(base_format_test)),
                       PlainText("HoverEventShowItem ",
                                 hover_event=ShowItem({"id": "minecraft:command_block"})),
                       TranslatedText("translation.test.none"),
                       TranslatedText("translation.test.complex",
                                      [PlainText("1"), PlainText("2"), PlainText("3")]),
                       ScoreboardValue("*", "test"),
                       Selector("@e", separator=[PlainText("SEP", color="red")]),
                       Keybind("key.jump"),
                       NBT("Pos", entity="@e", separator=[PlainText("SEP", color="red")])))


if __name__ == '__main__':
    main()
