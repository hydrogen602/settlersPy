from __future__ import annotations
import json
from typing import Dict, Optional, List, Union


class ParseFailure(Exception):
    pass


class JsonParser:

    def __init__(self, jsonContent: Union[str, Dict[str, object]]):
        self.obj: Dict[str, object]

        if isinstance(jsonContent, str):
            self.obj = json.loads(jsonContent)
        else:
            self.obj = jsonContent
    
    def askName(self) -> Optional[str]:
        x = self.obj.get('__name__')
        if isinstance(x, str) or x is None:
            return x
        raise ParseFailure('Expected an str for name')
    
    def hasAttr(self, name) -> bool:
        x = self.obj.get(name)
        return x is not None
    
    def requireName(self, name):
        if not self.askName() == name:
            raise ParseFailure(f'Wrong name, got {self.askName()}, expected {name}')
    
    def requireString(self, name) -> str:
        x = self.obj.get(name)
        if isinstance(x, str):
            return x
        raise ParseFailure(f'Expected string, got {x}')

    def requireObject(self, name) -> JsonParser:
        x = self.obj.get(name)
        if isinstance(x, dict):
            return JsonParser(x)
        raise ParseFailure(f'Expected dict, got {x}')

    def requireList(self, name) -> list:
        x = self.obj.get(name)
        if isinstance(x, list):
            return x
        raise ParseFailure(f'Expected list, got {x}')


class JsonParserType:

    def __init__(self, jsonContent: Union[str, Dict[str, object]]):
        obj: JsonParser = JsonParser(jsonContent)

        self.type_: str = obj.requireString('type')
        self.content: str = obj.requireString('content')
        self.args: list = []
        
        if obj.hasAttr('args'):
            self.args = obj.requireList('args')
    
    def requireArgs(self, count: int) -> tuple:
        if len(self.args) != count:
            raise ParseFailure(f'Wrong args count, expected {count} but got {len(self.args)}')

        return tuple(self.args)
