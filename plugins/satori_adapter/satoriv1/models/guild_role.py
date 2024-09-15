from dataclasses import dataclass
from typing import Optional


@dataclass
class GuildRole:
    id: str
    name: Optional[str] = None
    