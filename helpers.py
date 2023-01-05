from pydantic import BaseModel, validator, conint


class QuizQuestion(BaseModel):
    question: str
    correct_answers: tuple[str, ...]
    wrong_answers: tuple[str, ...]


class QuizConfiguration(BaseModel):
    questions: list[QuizQuestion]
    question_per_page: conint(gt=0) = 1
    question_per_test: conint(gt=0) = 4

    @validator('question_per_test')
    def question_per_test_validation(cls, v, values, **kwargs) -> int:
        if 'questions' in values and v > len(values['questions']):
            raise ValueError('question_per_test is greater than total questions')
        return v


class QuizEnded(Exception):
    pass
    