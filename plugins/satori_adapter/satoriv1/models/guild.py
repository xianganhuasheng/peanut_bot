from dataclasses import dataclass
from typing import Optional


@dataclass
class Guild:
    id: int
    name: Optional[str] = None
    avatar: Optional[str] = None