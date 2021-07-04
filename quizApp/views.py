from quiz.services import QuizResultService
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalCreateView
)

from .forms import *
from .models import *
from quiz.dto import *


def index(request):

    if 'result' in request.session:
        request.session.pop('result')
        request.session.pop('answers')

    continue_button = True if 'answers' in request.session else False

    request.session['quiz_id'] = '1'
    return render(request, 'quizApp/index.html', {'continue_button': continue_button})


class LogInView(BSModalLoginView):
    form_class = CustomAuthenticationForm
    template_name = 'quizApp/login.html'
    next = reverse_lazy('index')


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'quizApp/signup.html'
    success_url = reverse_lazy('index')


def get_quiz_dto(quiz_id):

    quiz = Quiz.objects.get(pk=quiz_id)

    quiz_DTO = QuizDTO(
        uuid=str(quiz.id),
        title=quiz.title,
        questions=[
            QuestionDTO(
                uuid=str(question.id),
                text=question.text,
                choices=[
                    ChoiceDTO(
                        uuid=str(choice.id),
                        text=choice.text,
                        is_correct=choice.is_correct
                    ) for choice in Choice.objects.filter(question_id=question.id)
                ]
            ) for question in Question.objects.filter(quiz=quiz_id)
        ]
    )

    return quiz_DTO


def questionList(request):

    if 'quiz_id' not in request.session or 'result' in request.session:
        return redirect(index)

    quiz = get_quiz_dto(request.session['quiz_id'])

    answers = request.session['answers'] if 'answers' in request.session else {
    }

    return render(request, 'quizApp/question_list.html', {
        'questions': quiz.questions,
        'answers': answers
    })


def detail_view(request):

    if 'quiz_id' not in request.session or 'result' in request.session:
        return redirect(index)

    quiz = get_quiz_dto(request.session['quiz_id'])

    if 'answers' not in request.session:
        request.session['answers'] = {}

    answers = request.session['answers']

    paginator = Paginator(quiz.questions, 1)
    page_number = request.GET.get('q')
    page_obj = paginator.get_page(page_number)

    question_id = page_obj.object_list[0].uuid

    if request.method == 'POST':
        choices = request.POST.getlist('choice')

        answers[question_id] = choices
        request.session['answers'] = answers

    if question_id in answers and not answers[question_id]:
        answers.pop(question_id)

    return render(request, 'quizApp/detail.html', {
        'page_obj': page_obj,
        'answers': answers[question_id] if question_id in answers else []
    })


def results(request):

    if 'quiz_id' not in request.session:
        return redirect(index)

    quiz_dto = get_quiz_dto(request.session['quiz_id'])

    if 'answers' not in request.session:
        result = 0
    else:
        answers = request.session['answers']

        answers_dto = AnswersDTO(
            quiz_uuid=request.session['quiz_id'],
            answers=[
                AnswerDTO(
                    question_uuid=key,
                    choices=answers[key]
                )
                for key in answers
            ]
        )
        quizResultService = QuizResultService(quiz_dto, answers_dto)
        result = int(quizResultService.get_result() * 100)
        request.session['result'] = result

    return render(request, 'quizApp/results.html', {'result': result})
