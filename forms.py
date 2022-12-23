from flask_wtf import FlaskForm as Form
from wtforms import SelectMultipleField
from wtforms.validators import ValidationError
from typing import Iterable
from random import shuffle

from helpers import QuizQuestion


class CorrectAnswer(object):
    def __init__(self, answer: tuple):
        self.answer = list(answer)

    def __call__(self, form, field):
        if field.data is None:
            raise ValidationError('Empty answer.')
        field.data.sort()
        self.answer.sort()
        if field.data != self.answer:
            raise ValidationError('Incorrect answer.')


def _form_class_generator(form_data: Iterable[SelectMultipleField]) -> Form:
    class StaticForm(Form):
        class Meta:
            csrf = False

    for x, _ in enumerate(form_data):
        setattr(StaticForm, 'q'+str(x), _)
    return StaticForm()


def build_form(form_data: Iterable[QuizQuestion]) -> Form:
    fields = []
    for _ in form_data:
        answers = list(_.correct_answers + _.wrong_answers)
        shuffle(answers)
        fields.append(SelectMultipleField(_.question, choices=answers, validators=[CorrectAnswer(_.correct_answers)]))
    return _form_class_generator(fields)
