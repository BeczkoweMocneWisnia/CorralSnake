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
    image = models.ImageField(upload_to=uuid_upload_to('quiz/images'), null=True)


class Question(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=10000)
    image = models.ImageField(upload_to=uuid_upload_to('questions/images'), null=True)
    question_type = models.CharField(blank=False, null=False, choices=QUESTION_TYPES, max_length=255)
    answer = models.CharField(max_length=255)
    question_answers = models.ManyToManyField('QuestionAnswer', related_name='answers')
    order = models.IntegerField(default=0)


class QuestionAnswer(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(default=0)


class SubmittedAnswer(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255, null=True)
    question_answers = models.ManyToManyField(QuestionAnswer, related_name='submitted_answers')

