import json
from abc import ABC, abstractmethod
from hashlib import sha256
from pathlib import Path


class Users(ABC):
    @abstractmethod
    def check_login(self, username: str, password: str) -> bool:
        raise NotImplementedError


class UsersFromJSON(Users):
    def __init__(self, file: Path) -> None:
        with open(file, 'rt') as f:
            self.users = json.loads(f.read())
        f.close()

    def check_login(self, username: str, password: str) -> bool:
        try:
            if sha256(password.encode()).hexdigest() == self.users[username]:
                return True
        except KeyError:
            return False
        return False
