from flask_wtf import FlaskForm as Form
from wtforms import SelectMultipleField,StringField
from wtforms.validators import ValidationError, NumberRange
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

class PopQuiz(Form):
    class Meta:
        csrf = False

    title = 'TEST'

    @classmethod
    def builder(cls, data):
        i = 0
        for line in data.question:
            i += 1
            chcs=line['answers']['true']+line['answers']['false']
            random.shuffle(chcs)
            setattr(cls,'q'+str(i),SelectMultipleField(line['question'],
                                              choices=chcs,
                                              validators=[CorrectAnswer(line['answers']['true'])]))

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
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @staticmethod
    def fromJSON(json_dct):
      return Quiz(from_json=True, data=json.loads(json_dct))

    @property
    def question(self):
        question = []
        for i in range(0,self.question_per_page):
            try:
                question.append(self.set.pop())
            except IndexError:
                raise IndexError('Set ended')
        return question

