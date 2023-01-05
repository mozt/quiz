import random
from pathlib import Path

from helpers import (QuizConfiguration, QuizEnded, QuizQuestion)


class Quiz(object):
    def __init__(self, 
                 file: Path | None = None, 
                 json_dct: str | bytes | bytearray | None = None) -> None:
        if json_dct is not None:
            self.quiz = QuizConfiguration.parse_raw(json_dct)
        elif file is not None:
            with open(file, 'rt') as f:
                self.quiz = QuizConfiguration.parse_raw(f.read())
            f.close()
            if self.quiz.question_per_test <= len(self.quiz.questions):
                self.quiz.questions = random.sample(self.quiz.questions,
                                                self.quiz.question_per_test)
            else:
                random.shuffle(self.quiz.questions)
        else:
            raise NotImplementedError

    def to_json(self) -> str:
        return self.quiz.json()

    @staticmethod
    def from_json(json_dct: str | bytes | bytearray) -> "Quiz":
        return Quiz(json_dct=json_dct)

    @property
    def question(self) -> list[QuizQuestion]:
        try:
            return [self.quiz.questions[_] for _ in range(self.quiz.question_per_page)]
        except IndexError:
            if self.quiz.questions: return self.quiz.questions
            raise QuizEnded('Quiz ended')
                

    def pop_questions(self) -> None:
        try:
            del self.quiz.questions[:self.quiz.question_per_page]
        except IndexError:
            raise QuizEnded('Quiz ended')
