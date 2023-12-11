from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.models import Note
from .test_routes import BaseClass

User = get_user_model()


class TestMajor(BaseClass):

    def setUp(self):
        self.note = Note.objects.create(
            title='Заметка',
            text='Просто текст.',
            slug='test_slug_1',
            author=self.author,
        )

    def test_note_in_list_for_author(self):
        response = self.author_client.get(self.LIST_URL)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_note_not_in_list_for_reader(self):
        response = self.reader_client.get(self.LIST_URL)
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)

    def test_page_contains_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
