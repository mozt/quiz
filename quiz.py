from flask_wtf import FlaskForm as Form
from wtforms import SelectMultipleField
from wtforms.validators import ValidationError
import json
import random


class CorrectAnswer(object):
    def __init__(self, answer):
        self.answer = answer

    def __call__(self, form, field):
        message = 'Incorrect answer.'
        field.data.sort()
        self.answer.sort()
        if field.data != self.answer:
            raise ValidationError(message)


class Quiz(object):
    def __init__(self, file=None, from_json=False, data=None):
        if from_json:
            self.set = data['set']
            self.question_per_page = data['question_per_page']
        else:
            with open(file, 'rt') as f:
                data = json.loads(f.read())
                self.set = random.sample(data['questions'], data['question-per-test'])
                self.question_per_page = data['question-per-page']
                random.shuffle(self.set)
            f.close()

    def toJSON(self) -> bytes:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @staticmethod
    def fromJSON(json_dct) -> object:
        return Quiz(from_json=True, data=json.loads(json_dct))

    @property
    def question(self) -> list:
        question = []
        for _ in range(0, self.question_per_page):
            try:
                question.append(self.set[_])
            except IndexError:
                raise IndexError('Set ended')
        return question

    def PopQuiz(self, pop=False) -> Form:
        class StaticForm(Form):
            class Meta:
                csrf = False

        if pop:
            for _ in range(0, self.question_per_page):
                self.set.pop(0)
        i = 0
        for _ in self.question:
            i += 1
            chcs = _['answers']['true']+_['answers']['false']
            random.shuffle(chcs)
            setattr(StaticForm, 'q'+str(i), SelectMultipleField(_['question'], choices=chcs, validators=[CorrectAnswer(_['answers']['true'])]))
        return StaticForm()
