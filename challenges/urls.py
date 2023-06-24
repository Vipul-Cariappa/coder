from django.urls import path

from . import views

app_name = "challenge"


urlpatterns = [
    path("question_submit/", views.question_submit, name="new_question"),
    path("questions_list/", views.questions_list, name="list_question"),
    path('answer_submit/<int:question_id>', views.answer_submit, name='answer'),
    path('answers_list/<int:question_id>', views.answers_list, name='list_answer'),
]
