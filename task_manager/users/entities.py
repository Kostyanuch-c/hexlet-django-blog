from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserEntity:
    id: int  # noqa
    username: str
    first_name: str
    last_name: str
    full_name: str
    created_at: datetime


@dataclass
class UserInput:
    first_name: str
    last_name: str
    username: str
    password: str
