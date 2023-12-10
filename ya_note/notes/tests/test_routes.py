from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class TestMajor(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='test_note',
            author=cls.author,
        )
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.user = User.objects.create(username='Миролюб')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)

    def test_home_page(self):
        users = (
            self.author,
            self.user,
            self.client
        )
        urls = (
            (
                'notes:home',
                False,
                {
                    self.author: HTTPStatus.OK,
                    self.user: HTTPStatus.OK,
                    self.client: HTTPStatus.OK,
                }
            ),
            (
                'users:login',
                False,
                {
                    self.author: HTTPStatus.OK,
                    self.user: HTTPStatus.OK,
                    self.client: HTTPStatus.OK,
                }
            ),
            (
                'users:logout',
                False,
                {
                    self.author: HTTPStatus.OK,
                    self.user: HTTPStatus.OK,
                    self.client: HTTPStatus.OK,
                }
            ),
            (
                'users:signup',
                False,
                {
                    self.author: HTTPStatus.OK,
                    self.user: HTTPStatus.OK,
                    self.client: HTTPStatus.OK,
                }
            ),
            (
                'notes:add',
                False,
                {
                    self.author: HTTPStatus.OK,
                    self.user: HTTPStatus.OK,
                    self.client: HTTPStatus.FOUND,
                }
            ),
            (
                'notes:list',
                False,
                {
                    self.author: HTTPStatus.OK,
                    self.user: HTTPStatus.OK,
                    self.client: HTTPStatus.FOUND,
                }
            ),
            (
                'notes:success',
                False,
                {
                    self.author: HTTPStatus.OK,
                    self.user: HTTPStatus.OK,
                    self.client: HTTPStatus.FOUND,
                }
            ),
            (
                'notes:detail',
                True,
                {
                    self.author: HTTPStatus.OK,
                    self.user: HTTPStatus.NOT_FOUND,
                    self.client: HTTPStatus.FOUND,
                }
            ),
            (
                'notes:edit',
                True,
                {
                    self.author: HTTPStatus.OK,
                    self.user: HTTPStatus.NOT_FOUND,
                    self.client: HTTPStatus.FOUND,
                }
            ),
            (
                'notes:delete',
                True,
                {
                    self.author: HTTPStatus.OK,
                    self.user: HTTPStatus.NOT_FOUND,
                    self.client: HTTPStatus.FOUND,
                }
            ),
        )
        for user in users:
            for name, args, expected_status in urls:
                if user != self.client:
                    self.auth_client.force_login(user)
                with self.subTest(name=name):
                    url = reverse(
                        name, args=((self.note.slug,) if args else None)
                    )
                    response = self.auth_client.get(url)
                    self.assertEqual(
                        response.status_code, expected_status[user]
                    )

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        urls = (
            ('notes:list', None),
            ('notes:success', None),
            ('notes:add', None),
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
