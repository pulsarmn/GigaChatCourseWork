from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
