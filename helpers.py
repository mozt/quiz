from pydantic import BaseModel, conint


class QuizQuestion(BaseModel):
    question: str
    correct_answers: tuple[str, ...]
    wrong_answers: tuple[str, ...]


class QuizConfiguration(BaseModel):
    question_per_test: conint(gt=0) = 4
    question_per_page: conint(gt=0) = 1
    questions: list[QuizQuestion]


# class QuizConfigurationFromSource(QuizConfigurationFromSession):
#     @validator('questions')
#     def questions_load_only_requested_num(cls, v, values, **kwargs) -> int:
#         if 'question_per_test' in values:
#             return random.sample(v, values['question_per_test'])
#         return v

#     @validator('question_per_test')
#     def question_per_test_validation(cls, v, values, **kwargs) -> int:
#         if 'questions' in values and v > len(values['questions']):
#             raise ValueError(
#                 'question_per_test is greater than total questions')
#         return v


class QuizEnded(Exception):
    pass
    