from django import forms

from .models import Answer, Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = (
            "title",
            "question",
            "difficulty",
            "start_snippet",
            "solution",
            "test_case",
        )

        help_texts = {
            "title": "Give a meaning full title to the question",
            "question": "Describe the question. Provide some examples for specific inputs",
            "start_snippet": "Add a starting code block to help the user start to solve the question",
            "solution": "Provide your solution for our system to verify",
            "test_case": "Provide test cases to check against if the given solution is correct",
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("answer",)
