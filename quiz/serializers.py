from django.contrib.auth import get_user_model
from rest_framework import serializers

from article.models import Article
from article.serializers import ArticleSerializer
from quiz.models import Quiz, SubmittedAnswer, QuestionAnswer, Question
from user.serializers import FriendSerializer

User = get_user_model()


class QuizSerializer(serializers.ModelSerializer):
    author = FriendSerializer(many=False, read_only=True)
    author_pk = serializers.SlugRelatedField(
        source='author', queryset=User.objects.all(), slug_field='pk', write_only=True
    )

    article = ArticleSerializer(many=False, read_only=True)
    article_public_id = serializers.SlugRelatedField(
        source='article', queryset=Article.objects.all(), slug_field='public_id', write_only=True
    )

    class Meta:
        model = Quiz
        fields = [
            'public_id',
            'author',
            'author_pk',
            'title',
            'description',
            'article',
            'article_public_id'
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
    quiz = ArticleSerializer(many=False, read_only=True)
    quiz_public_id = serializers.SlugRelatedField(
        source='quiz', queryset=Quiz.objects.all(), slug_field='public_id', write_only=True
    )

    class Meta:
        model = Question
        fields = [
            'public_id',
            'quiz',
            'quiz_public_id',
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
    question = QuestionSerializer(many=False, read_only=True)
    question_public_id = serializers.SlugRelatedField(
        source='question', queryset=Question.objects.all(), slug_field='public_id', write_only=True
    )

    class Meta:
        model = QuestionAnswer
        fields = [
            'public_id',
            'question',
            'value',
            'question',
            'question_public_id'
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


class SubmittedAnswerSerializer(SubmitterAnswerBasicSerializer):
    question = QuestionSerializer(many=False, read_only=True)
    question_public_id = serializers.SlugRelatedField(
        source='question', queryset=Question.objects.all(), slug_field='public_id', write_only=True
    )

    question_answers = serializers.SlugRelatedField(
        many=True,
        queryset=QuestionAnswer.objects.all(),
        slug_field='public_id'
    )

    class Meta:
        model = SubmittedAnswer
        fields = [
            'public_id',
            'question',
            'question_public_id',
            'answer',
            'question_answers',
        ]
        read_only_fields = ['public_id']


class QuestionWithPossibleAnswersSerializer(QuestionBasicSerializer):
    possible_answers = QuestionAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            'public_id',
            'title',
            'description',
            'question_type',
            'answer',
            'possible_answers'
        ]
        read_only_fields = ['public_id']


class QuizFullSerializer(serializers.ModelSerializer):
    author = FriendSerializer(many=False, read_only=True)
    article = serializers.SlugRelatedField(
        queryset=Article.objects.all(),
        slug_field='public_id'
    )
    questions = QuestionWithPossibleAnswersSerializer(many=True, read_only=True)

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
            'question_answers',
        ]
        read_only_fields = ['public_id']
