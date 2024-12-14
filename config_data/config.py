from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str

@dataclass
class Config:
    tg_bot: TgBot
    payment_token: str

    gigachat_token: str
