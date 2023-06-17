from django.urls import path

from . import views

app_name = "challenge"


urlpatterns = [
    path("new_question/", views.create_question, name="new_question"),
    path("list_question/", views.list_questions, name="list_question"),
    path('answer/<int:question_id>', views.answer, name='answer'),
    path('update_answer/<int:answer_id>', views.update_answer, name='update_answer'),
    path('list_answer/<int:question_id>', views.list_answers, name='list_answer'),
]
