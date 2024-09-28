from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from article.models import Article
from quiz.models import Quiz, Question, QuestionAnswer, SubmittedAnswer
from user.models import USER_ROLES

User = get_user_model()


class QuizTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(email='admin@admin.com',
                                                  username='testuser',
                                                  password='testpass',
                                                  role="Teacher")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_quiz(self):
        article = Article.objects.create(author=self.user, title='title', description='description')

        data = {
            "title": "Quiz",
            "description": "Quiz desc",
            "article_public_id": article.public_id
        }

        response = self.client.post('/quiz/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 1)

    def test_add_question(self):
        article = Article.objects.create(author=self.user, title='title', description='description')
        quiz = Quiz.objects.create(author=self.user, title='title', description='description', article=article)

        data = {
            "title": "Quiz",
            "description": "Quiz desc",
            "quiz_public_id": quiz.public_id,
            "question_type": "S",
            "answer": "30",
            "order": 1
        }

        response = self.client.post('/quiz/question/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)

    def test_add_answer(self):
        article = Article.objects.create(author=self.user, title='title', description='description')
        quiz = Quiz.objects.create(author=self.user, title='title', description='description', article=article)
        question = Question.objects.create(quiz=quiz,
                                           title="Quiz",
                                           description="Quiz desc",
                                           question_type="S",
                                           answer="30",
                                           order=1)

        data = {
            "question_public_id": question.public_id,
            "value": 30
        }

        response = self.client.post('/quiz/question/answer/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(QuestionAnswer.objects.count(), 1)

    def test_add_submitted_answer(self):
        article = Article.objects.create(author=self.user, title='title', description='description')
        quiz = Quiz.objects.create(author=self.user, title='title', description='description', article=article)
        question = Question.objects.create(quiz=quiz,
                                           title="Quiz",
                                           description="Quiz desc",
                                           question_type="S",
                                           order=1)
        question_answers = QuestionAnswer.objects.create(question=question, value=9)

        question.question_answers.set([question_answers])
        question.save()

        data = {
            "question_public_id": question.public_id,
            "question_answers": [question_answers.public_id],
        }

        response = self.client.post('/quiz/question/answer/submit/', data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SubmittedAnswer.objects.count(), 1)
