from dataclasses import dataclass
from typing import Tuple


@dataclass
class QuizQuestion:
    question: str
    correct_answers: Tuple[str, ...]
    wrong_answers: Tuple[str, ...]

class QuizEnded(Exception):
    pass
    