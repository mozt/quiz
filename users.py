import json
from pathlib import Path
from hashlib import sha256


class Users(object):
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
