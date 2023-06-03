from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):
    """
    Contents tests.
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Пользователь')
        cls.author = User.objects.create(username='Автор')
        cls.note = Note.objects.create(
            title='Заметка',
            text='Текст',
            slug='test-slug',
            author=cls.author
        )

    def test_note_list(self):
        """
        Tests of note in notes list.
        Some notes didn't go to another authors list.
        """
        users = (
            (self.author, True),
            (self.user, False),
        )
        for user, expected_notes in users:
            with self.subTest(user=user):
                self.client.force_login(user)
                response = self.client.get(reverse('notes:list'))
                notes = response.context['object_list']
                self.assertEqual((self.note in notes), expected_notes)

    def test_authorized_client_has_form(self):
        """
        Tests form.
        """
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for name, args in urls:
            with self.subTest(name=name):
                self.client.force_login(self.author)
                url = reverse(name, args=args)
                response = self.client.get(url)
                form = response.context['form']
                self.assertIn('form', response.context)
                self.assertIsInstance(form, NoteForm)
