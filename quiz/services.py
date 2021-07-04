from .dto import ChoiceDTO, QuestionDTO, QuizDTO, AnswerDTO, AnswersDTO
from typing import List


class QuizResultService():
    def __init__(self, quiz_dto: QuizDTO, answers_dto: AnswersDTO):
        self.quiz_dto = quiz_dto
        self.answers_dto = answers_dto

    def get_result(self) -> float:
        result = 0
        answers = self.answers_dto.answers
        questions = self.quiz_dto.questions
        correct_answers, submitted_answers = {}, {}

        for question in questions:
            correct_answers[question.uuid] = [
                choice.uuid
                for choice in filter(lambda x: x.is_correct, question.choices)
            ]

        for answer in answers:
            submitted_answers[answer.question_uuid] = answer.choices

        for key in submitted_answers:
            if correct_answers[key] == submitted_answers[key]:
                result += 1/len(questions)

        return result
