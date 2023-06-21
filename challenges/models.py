from django.contrib.auth.models import User
from django.db import models

QUESTION_DIFFICULTY = (
    ("HARD", "HARD"),
    ("MEDIUM", "MEDIUM"),
    ("EASY", "EASY"),
)


# Create your models here.
class Question(models.Model):
    title = models.CharField(max_length=200, unique=True)
    question = models.TextField()
    questionHTML = models.TextField()
    solution = models.TextField()
    test_case = models.TextField()
    test_case_string = models.TextField()
    start_snippet = models.TextField()
    start_snippet_string = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    question_verified = models.BooleanField(default=False)
    upload_time = models.DateTimeField(auto_now_add=True)
    users_attempted = models.IntegerField(default=0)
    users_completed = models.IntegerField(default=0)
    difficulty = models.CharField(max_length=20, choices=QUESTION_DIFFICULTY)

    def __str__(self):
        return f"{self.title}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    answer = models.TextField()
    answer_string = models.TextField()
    answer_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.question.title} by {self.user.username}"
