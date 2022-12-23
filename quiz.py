from pathlib import Path
from typing import List, Dict
import json
import random

from helpers import QuizQuestion, QuizEnded


class Quiz(object):
    def __init__(
            self,
            file: Path | None = None,
            json_dct: str | bytes | bytearray | None = None,
    ) -> None:
        if json_dct is not None:
            data: Dict = json.loads(json_dct)
        elif file is not None:
            with open(file, 'rt') as f:
                data = json.loads(f.read())
            f.close()
        else:
            raise NotImplementedError
        self.question_per_page = data['question_per_page']
        self.question_per_test = data['question_per_test']
        self.questions = []
        for _ in random.sample(data['questions'], self.question_per_test) if file is not None else data['questions']:
            self.questions.append(QuizQuestion(
                question=_['question'], 
                correct_answers=tuple(_['correct_answers']), 
                wrong_answers=tuple(_['wrong_answers'])))

    def _serialization_filter(self) -> Dict:
        result = {}
        for k, v in self.__dict__.items():
            if k not in ('form_builder',):
                result[k] = v
        return result

    def to_json(self) -> str:
        return json.dumps(
            self._serialization_filter(),
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

    @staticmethod
    def from_json(json_dct: str | bytes | bytearray) -> "Quiz":
        return Quiz(json_dct=json_dct)

    @property
    def question(self) -> List[QuizQuestion]:
        question = []
        for _ in range(0, self.question_per_page):
            try:
                question.append(self.questions[_])
            except IndexError:
                raise QuizEnded('Quiz ended')
        return question

    def pop_questions(self) -> None:
        for _ in range(0, self.question_per_page):
            self.questions.pop(0)
