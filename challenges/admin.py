from django.contrib import admin

from .models import Answer, Question, AnswerComments, QuestionComments

# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuestionComments)
admin.site.register(AnswerComments)
