import json
from dataclasses import dataclass

import typing

PREFIX = "prefix"
OBJECT = "object"
MAPPING = "mappings"


class Mapping:
    source: str
    destination: str

    def __init__(self, source, destination) -> None:
        self.source = source
        self.destination = destination


MappingList = typing.List[Mapping]


@dataclass
class Config:
    object_str = None
    mappings_obj: MappingList = None
    prefix_str = None

    def __init__(self, object_str, mappings_obj, prefix_str) -> None:
        self.object_str = object_str
        self.mappings_obj = mappings_obj
        self.prefix_str = prefix_str


def create_mapping_obj(maps):
    mappings = []
    for obj in maps:
        s = obj.get('source')
        d = obj.get('destination')
        mapping = Mapping(s, d)
        mappings.append(mapping)
    return mappings


class Parser:
    def __init__(self, file_path) -> None:
        with open(file_path, "r", encoding="utf-8")as f:
            self.config = json.load(f)

    def validate(self):
        prefix_str = self.config.get(PREFIX)
        if prefix_str is None:
            raise Exception('Prefix not providen.')
        if type(prefix_str) != str:
            raise Exception('Invalid Prefix')
        object_str = self.config.get(OBJECT)
        if object_str is None:
            raise Exception('Object not providen.')
        if type(object_str) != str:
            raise Exception('Invalid object')
        mapping_obj = self.config.get(MAPPING)
        if mapping_obj is None:
            raise Exception('Mappings not providen.')
        if type(mapping_obj) != list:
            raise Exception('Invalid mapping')

        return Config(
            prefix_str=prefix_str,
            object_str=object_str,
            mappings_obj=create_mapping_obj(mapping_obj)
        )


if __name__ == "__main__":
    p = Parser("../data/sample.json")
    conf = p.validate()
    print(conf.mappings_obj)
    print(conf.object_str)
    print(conf.prefix_str)
