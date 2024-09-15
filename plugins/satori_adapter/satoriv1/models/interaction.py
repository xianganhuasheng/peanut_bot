from dataclasses import dataclass


@dataclass
class Argv:
    name: str
    arguments: any
    options: object


@dataclass
class Button:
    id: str