import uuid

from django.db import models

from CorralSnake.utils import uuid_upload_to


QUESTION_TYPES = {
    "S": "Single",
    "M": "Multiple",
    "O": "Open",
}


class Quiz(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey('user.User', on_delete=models.CASCADE)
    article = models.ForeignKey('article.Article', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=10000)
    image = models.ImageField(upload_to=uuid_upload_to('quiz/images'))


class Question(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=10000)
    image = models.ImageField(upload_to=uuid_upload_to('questions/images'))
    question_type = models.CharField(blank=False, null=False, choices=QUESTION_TYPES, max_length=255)
    answer = models.CharField(max_length=255)
    order = models.IntegerField(default=0)


class QuestionAnswer(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)


class SubmittedAnswer(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    question_answer = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE)
