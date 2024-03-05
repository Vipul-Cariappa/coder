from django.urls import path

from . import views

app_name = "challenge"


urlpatterns = [
    path("question_submit/", views.question_submit, name="new_question"),
    path("questions_list/", views.questions_list, name="list_question"),
    path("questions_list/<str:difficulty>", views.questions_list, name="list_question_difficulty"),
    path("question_view/<int:question_id>", views.question_view, name="question_view"),
    path("question_comment/<int:question_id>", views.question_post_comment, name="question_comment"),
    path("question_like/<int:question_id>", views.question_like, name="question_like"),
    path("answer_submit/<int:question_id>", views.answer_submit, name="answer"),
    path("answers_list/<int:question_id>", views.answers_list, name="list_answer"),
    path("answer_view/<int:answer_id>", views.answer_view, name="answer_view"),
    path("answer_comment/<int:answer_id>", views.answer_post_comment, name="answer_comment"),
    path("answer_like/<int:answer_id>", views.answer_like, name="answer_like"),
]
