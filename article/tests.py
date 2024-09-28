from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from article.models import Article
from user.models import USER_ROLES

User = get_user_model()


class ArticleTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(email='admin@admin.com',
                                                  username='testuser',
                                                  password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_article(self):
        student = User.objects.create_user(email='not@admin.com',
                                                  username='testusertwo',
                                                  password='testpasstwo',
                                                  role=USER_ROLES["Student"]
                                                  )
        self.client.force_authenticate(user=student)

        data = {
            "title": "Test",
            "description": "Test",
        }

        response = self.client.post('/article/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.count(), 0)

    def test_create_bad_article(self):
        student = User.objects.create_user(email='not@admin.com',
                                                  username='testusertwo',
                                                  password='testpasstwo',
                                                  role=USER_ROLES["Teacher"]
                                                  )
        self.client.force_authenticate(user=student)

        data = {
            "title": "Test",
            "description": "Test",
        }

        response = self.client.post('/article/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 1)