from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from users.models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone='+79280096181',
            email='test@test.com',
            first_name="admin",
            last_name="admin",
            password='12345'
        )
        # self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        new_user = User.objects.create(
            phone='+7928096180',
            email='test@test1.com',
            first_name="admin1",
            last_name="admin1",
            password='123'
        )

        self.assertEqual(new_user.email, 'test@test1.com')
        self.assertEqual(new_user.first_name, 'admin1')
        self.assertEqual(new_user.phone, '+7928096180')

    def test_user_update(self):
        self.user.email = 'test@test2.com'
        self.user.phone = '+7928096182'
        self.user.first_name = 'admin2'
        self.user.last_name = 'admin2'
        self.user.save()

        self.assertEqual(self.user.email, 'test@test2.com')
        self.assertEqual(self.user.phone, '+7928096182')
        self.assertEqual(self.user.first_name, 'admin2')
        self.assertEqual(self.user.last_name, 'admin2')

    def test_user_delete(self):
        self.user.delete()
        self.assertEqual(User.objects.count(), 0)


class RegisterUserTestCase(TestCase):
    def setUp(self):
        pass

    def test_form_register(self):
        path = reverse('users:register')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_form_register_success(self):

        data = {
            'phone': '+79280096183',
            'email': 'test@test.com',
            'first_name': 'admin',
            'last_name': 'admin',
            'password1': '12345',
            'password2': '12345'
        }
        user_model = get_user_model()
        path = reverse('users:register')
        response = self.client.post(path, data)
        print(response.status_code)
        self.assertEqual(response.status_code, HTTPStatus.OK)






