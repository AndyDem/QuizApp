from quizApp.models import Question
from django.contrib import admin
from .models import *

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Quiz)
