from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

User = get_user_model()


class UserTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        data = {
            "email": "newuser@test.com",
            "username": "newuser",
            "password": "StrongPassword$123",
            "role": "Teacher"
        }
        response = self.client.post('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@test.com").exists())

    def test_user_login(self):
        user = User.objects.create_user(email='login@test.com', username='loginuser', password='loginpass123')
        data = {
            "email": "login@test.com",
            "password": "loginpass123"
        }
        response = self.client.post('/auth/token/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_data(self):
        user = User.objects.create_user(email='update@test.com', username='updateuser', password='updatepass123')
        self.client.force_authenticate(user=user)

        updated_data = {
            "first_name": "first_name"
        }
        response = self.client.patch(f'/user/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertEqual(user.first_name, 'first_name')

    def test_delete_user(self):
        user = User.objects.create_user(email='delete@test.com', username='deleteuser', password='deletepass123')
        self.client.force_authenticate(user=user)

        response = self.client.delete(f'/user/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=user.id).exists())
