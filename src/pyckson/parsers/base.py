from decimal import Decimal
from enum import Enum

class ParserException(Exception):
    pass


class Parser:
    def parse(self, json_value):
        pass


class BasicParser(Parser):
    def parse(self, json_value):
        return json_value


class BasicParserWithCast(Parser):
    def __init__(self, cls):
        self.cls = cls

    def parse(self, json_value):
        if not isinstance(json_value, self.cls):
            raise ParserException(f'"{json_value}" is supposed to be a {self.cls.__name__}.')
        return self.cls(json_value)


class ListParser(Parser):
    def __init__(self, sub_parser: Parser):
        self.sub_parser = sub_parser
        self.cls = list

    def parse(self, json_value):
        if not isinstance(json_value, list):
            raise ParserException(f'"{json_value}" is supposed to be a list.')
        return [self.sub_parser.parse(item) for item in json_value]


class SetParser(Parser):
    def __init__(self, sub_parser: Parser):
        self.sub_parser = sub_parser
        self.cls = set

    def parse(self, json_value):
        if not isinstance(json_value, set) and not isinstance(json_value, list):
            raise ParserException(f'"{json_value}" is supposed to be a set or a list.')
        return {self.sub_parser.parse(item) for item in json_value}


class DefaultEnumParser(Parser):
    def __init__(self, cls):
        self.cls = cls

    def parse(self, value):
        if value not in self.cls.__members__:
            raise ParserException(f'"{value}" is not a valid value for "{self.cls.__name__}" Enum.')
        return self.cls[value]


class CaseInsensitiveEnumParser(Parser):
    def __init__(self, cls):
        self.values = {member.name.lower(): member for member in cls}
        self.cls = Enum

    def parse(self, value):
        if value.lower() not in self.values:
            raise ParserException(f'"{value}" is not a valid value for "{self.cls.__name__}" Enum.')
        return self.values[value.lower()]


class ValuesEnumParser(Parser):
    def __init__(self, cls):
        self.cls = cls

    def parse(self, value):
        return self.cls(value)


class BasicDictParser(Parser):
    def parse(self, json_value):
        return json_value


class TypingDictParser(Parser):
    def __init__(self, value_parser: Parser):
        self.value_parser = value_parser

    def parse(self, json_value):
        return {k: self.value_parser.parse(v) for k, v in json_value.items()}


class DecimalParser(Parser):
    def parse(self, json_value):
        return Decimal(json_value)


class UnionParser(Parser):
    def __init__(self, value_parsers: list[Parser]):
        self.value_parsers = value_parsers

    def parse(self, json_value):
        for parser in self.value_parsers:
            if hasattr(parser, 'cls') and isinstance(json_value, parser.cls):
                return parser.parse(json_value)
        raise TypeError(f'{json_value} is not compatible with Union type in Pyckson.')
