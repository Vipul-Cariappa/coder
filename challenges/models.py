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
    start_snippet = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    question_verified = models.BooleanField(default=False)
    upload_time = models.DateTimeField(auto_now_add=True)
    users_attempted = models.ManyToManyField(User, related_name="users_attempted")
    users_completed = models.ManyToManyField(User, related_name="users_completed")
    difficulty = models.CharField(max_length=20, choices=QUESTION_DIFFICULTY, default="EASY", null=False, blank=False)

    def __str__(self):
        return f"{self.title}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    answer = models.TextField()
    answer_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tests_pass = models.BooleanField()

    def __str__(self):
        return f"{self.question.title} by {self.user.username}"
