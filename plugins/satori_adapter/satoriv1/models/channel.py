from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class Channel():

    class Type(Enum):
        TEXT = 0
        DIRECT = 1
        CATEGORY = 2
        VOICE = 3

    id: str
    type: Type
    name: Optional[str] = None
    parent_id: Optional[str] = None




