from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('detail/', views.detail_view, name='detail'),
    path('results/', views.results, name='results'),
    path('question_list', views.questionList, name='question_list'),
    path("logout/", LogoutView.as_view(), name='logout')
]