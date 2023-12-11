from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class BaseClass(TestCase):

    LIST_URL = reverse('notes:list')
    LOGIN_URL = reverse('users:login')
    ADD_URL = reverse('notes:add')

    form_data = {
        'title': 'Новый заголовок',
        'text': 'Новый текст',
        'slug': 'new-slug',
    }

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)


class TestMajor(BaseClass):

    def setUp(self):
        self.note = Note.objects.create(
            title='Заметка',
            text='Просто текст.',
            slug='test_slug_1',
            author=self.author,
        )

    def test_home_page(self):
        test_data = (
            (
                'notes:home',
                None,
                self.author,
                HTTPStatus.OK
            ),
            (
                'users:login',
                None,
                self.author,
                HTTPStatus.OK
            ),
            (
                'users:logout',
                None,
                self.author,
                HTTPStatus.OK
            ),
            (
                'users:signup',
                None,
                self.author,
                HTTPStatus.OK
            ),
            (
                'notes:add',
                None,
                self.author,
                HTTPStatus.OK
            ),
            (
                'notes:list',
                None,
                self.author,
                HTTPStatus.OK
            ),
            (
                'notes:success',
                None,
                self.author,
                HTTPStatus.OK
            ),
            (
                'notes:detail',
                (self.note.slug,),
                self.author,
                HTTPStatus.OK
            ),
            (
                'notes:edit',
                (self.note.slug,),
                self.author,
                HTTPStatus.OK
            ),
            (
                'notes:delete',
                (self.note.slug,),
                self.author,
                HTTPStatus.OK
            ),
            (
                'notes:home',
                None,
                self.reader,
                HTTPStatus.OK
            ),
            (
                'users:login',
                None,
                self.reader,
                HTTPStatus.OK
            ),
            (
                'users:logout',
                None,
                self.reader,
                HTTPStatus.OK
            ),
            (
                'users:signup',
                None,
                self.reader,
                HTTPStatus.OK
            ),
            (
                'notes:add',
                None,
                self.reader,
                HTTPStatus.OK
            ),
            (
                'notes:list',
                None,
                self.reader,
                HTTPStatus.OK
            ),
            (
                'notes:success',
                None,
                self.reader,
                HTTPStatus.OK
            ),
            (
                'notes:detail',
                (self.note.slug,),
                self.reader,
                HTTPStatus.NOT_FOUND
            ),
            (
                'notes:edit',
                (self.note.slug,),
                self.reader,
                HTTPStatus.NOT_FOUND
            ),
            (
                'notes:delete',
                (self.note.slug,),
                self.reader,
                HTTPStatus.NOT_FOUND
            ),
            (
                'notes:home',
                None,
                self.client,
                HTTPStatus.OK
            ),
            (
                'users:login',
                None,
                self.client,
                HTTPStatus.OK
            ),
            (
                'users:logout',
                None,
                self.client,
                HTTPStatus.OK
            ),
            (
                'users:signup',
                None,
                self.client,
                HTTPStatus.OK
            ),
            (
                'notes:add',
                None,
                self.client,
                HTTPStatus.FOUND
            ),
            (
                'notes:list',
                None,
                self.client,
                HTTPStatus.FOUND
            ),
            (
                'notes:success',
                None,
                self.client,
                HTTPStatus.FOUND
            ),
            (
                'notes:detail',
                (self.note.slug,),
                self.client,
                HTTPStatus.FOUND
            ),
            (
                'notes:edit',
                (self.note.slug,),
                self.client,
                HTTPStatus.FOUND
            ),
            (
                'notes:delete',
                (self.note.slug,),
                self.client,
                HTTPStatus.FOUND
            ),
        )
        for sample_data in test_data:
            name, args, user, status = sample_data
            if user != self.client:
                self.author_client.force_login(user)
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
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
                redirect_url = f'{self.LOGIN_URL}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
