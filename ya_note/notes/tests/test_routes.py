from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):
    """
    Urls tests.
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

    def test_pages_availability_for_auth_user(self):
        """
        Tests of access add notes, list notes and success pages for auth user.
        """
        urls = (
            'notes:add',
            'notes:list',
            'notes:success',
        )
        self.client.force_login(self.user)
        for name in urls:
            with self.subTest(user=self.user, name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability(self):
        """
        Tests of access homepage and logins pages for anonum.
        """
        urls = (
            'notes:home',
            'users:login',
            'users:logout',
            'users:signup',
        )
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_detail_and_edit_and_delete_notes(self):
        """
        Tests of access for detail page and edit and delete notes for author.
        """
        users_statuses = (
            (self.user, HTTPStatus.NOT_FOUND),
            (self.author, HTTPStatus.OK),
        )
        urls = (
            'notes:detail',
            'notes:edit',
            'notes:delete',
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in urls:
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        """
        Tests of redirects of anonum to login page.
        """
        login_url = reverse('users:login')
        urls = (
            ('notes:add', None),
            ('notes:list', None),
            ('notes:success', None),
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,))
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
