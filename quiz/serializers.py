from django.contrib.auth import get_user_model
from rest_framework import serializers

from article.models import Article
from quiz.models import Quiz, SubmittedAnswer, QuestionAnswer, Question
from user.serializers import FriendSerializer

User = get_user_model()


class QuizSerializer(serializers.ModelSerializer):
    author = FriendSerializer(many=False, read_only=True)
    author_pk = serializers.SlugRelatedField(
        source='author', queryset=User.objects.all(), slug_field='pk', write_only=True
    )

    class Meta:
        model = Quiz
        fields = [
            'public_id',
            'author',
            'author_pk'
            'title',
            'description',
            'image',
            'article',
        ]
        read_only_fields = ['public_id']


class QuestionBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'public_id',
            'title',
            'description',
            'image',
            'question_type',
            'answer'
        ]
        read_only_fields = ['public_id']


class QuestionSerializer(QuestionBasicSerializer):
    quiz = serializers.SlugRelatedField(
        queryset=Quiz.objects.all(),
        slug_field='public_id'
    )

    class Meta:
        model = Question
        fields = [
            'public_id',
            'quiz',
            'title',
            'description',
            'image',
            'question_type',
            'answer'
        ]
        read_only_fields = ['public_id']


class QuestionAnswerBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = [
            'public_id',
            'question',
            'value',
        ]
        read_only_fields = ['public_id']


class QuestionAnswerSerializer(QuestionAnswerBasicSerializer):
    question = serializers.SlugRelatedField(
        queryset=Question.objects.all(),
        slug_field='public_id'
    )

    class Meta:
        model = QuestionAnswer
        fields = [
            'public_id',
            'question',
            'value',
            'question',
        ]
        read_only_fields = ['public_id']


class SubmitterAnswerBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmittedAnswer
        fields = [
            'public_id',
            'answer',
        ]
        read_only_fields = ['public_id']


class SubmitterAnswerSerializer(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(
        queryset=Question.objects.all(),
        slug_field='public_id'
    )
    question_answer = serializers.SlugRelatedField(
        queryset=QuestionAnswer.objects.all(),
        slug_field='public_id'
    )

    class Meta:
        model = SubmittedAnswer
        fields = [
            'public_id',
            'question',
            'answer',
            'question_answer',
        ]
        read_only_fields = ['public_id']


class QuizFullSerializer(serializers.ModelSerializer):
    author = FriendSerializer(many=False, read_only=True)
    article = serializers.SlugRelatedField(
        queryset=Article.objects.all(),
        slug_field='public_id'
    )
    questions = QuestionBasicSerializer(many=True, read_only=True)
    question_answers = QuestionAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            'public_id',
            'author',
            'title',
            'description',
            'image',
            'article',
            'questions',
            'question_answers'
        ]
        read_only_fields = ['public_id']
