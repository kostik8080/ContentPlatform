from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from menenger.models import Content
from users.models import User


class ContentTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            phone='+79280096181',
            email='test@test.com',
            first_name="admin",
            last_name="admin",
            password='12345'
        )
        self.content = Content.objects.create(
            title="test",
            content="test",
            author=self.user,
        )

    def test_content_create(self):
        new_content = Content.objects.create(
            title="test1",
            content="test1",
            author=self.user,

        )
        self.assertEqual(new_content.title, "test1")
        self.assertEqual(new_content.content, "test1")
        self.assertEqual(new_content.author, self.user)
        self.assertTrue(new_content.pk)

    def test_content_list(self):
        content_list = Content.objects.all()
        self.assertEqual(content_list.count(), 1)
        self.assertEqual(content_list[0].title, "test")
        self.assertEqual(content_list[0].content, "test")
        self.assertEqual(content_list[0].author, self.user)
        self.assertTrue(content_list[0].pk)

    def test_content_update(self):
        self.content.title = "test1"
        self.content.content = "test1"
        self.content.save()
        self.assertEqual(self.content.title, "test1")
        self.assertEqual(self.content.content, "test1")
        self.assertEqual(self.content.author, self.user)
        self.assertTrue(self.content.pk)

    def test_content_delete(self):
        self.content.delete()
        self.assertEqual(Content.objects.all().count(), 0)


class ContentFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone='+79280096181',
            email='test@test.com',
            first_name="admin",
            last_name="admin",
            password='12345'
        )
        self.data = {
            'title': 'test',
            'content': 'test',
            'author': self.user.id,

        }

    def test_form_content(self):
        path = reverse('menenger:content_create')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'menenger/content_form.html')

    def test_form_register_success(self):

        path = reverse('menenger:content_create')
        response = self.client.post(path, self.data)
        print(response.status_code)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('menenger:home'))

