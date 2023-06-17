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
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    upload_time = models.DateTimeField()
    users_attempted = models.IntegerField()
    users_completed = models.IntegerField()
    difficulty = models.CharField(max_length=20, choices=QUESTION_DIFFICULTY)

    def __str__(self):
        return f"{self.title}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    answer = models.TextField()
    answer_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.question.title}"
