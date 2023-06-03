from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import WARNING
from news.models import Comment


@pytest.mark.django_db
def test_user_can_create_comment(author_client, author, form_data, news_pk):
    """
    Tests when author can create comments.
    """
    url = reverse('news:detail', args=news_pk)
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.author == author


def test_author_can_edit_comment(author_client, form_data, comment, news_pk):
    """
    Tests when author can edit comments.
    """
    url = reverse('news:edit', args=(comment.id,))
    redirect_url = reverse('news:detail', args=news_pk)
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{redirect_url}#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_author_can_delete_comment(author_client, comment, news_pk):
    """
    Tests when author can delete comments.
    """
    url = reverse('news:delete', args=(comment.id,))
    redirect_url = reverse('news:detail', args=news_pk)
    response = author_client.delete(url)
    assertRedirects(response, f'{redirect_url}#comments')
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(form_data, client, news_pk):
    """
    Tests when anonum can't create comments.
    """
    url = reverse('news:detail', args=news_pk)
    client.post(url, data=form_data)
    assert Comment.objects.count() == 0


def test_user_cant_edit_other_comment(admin_client, form_data, comment):
    """
    Tests when anonum can't edit comments.
    """
    url = reverse('news:edit', args=(comment.id,))
    response = admin_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_in_db = Comment.objects.get(id=comment.id)
    assert comment.text == comment_in_db.text


def test_user_cant_delete_other_comment(admin_client, comment):
    """
    Tests when anonum can't delete comments.
    """
    url = reverse('news:delete', args=(comment.id,))
    response = admin_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_count = Comment.objects.count()
    assert comment_count == 1


def test_user_cant_used_bad_words(author_client, bad_words_data, news_pk):
    """
    Tests of block bad words.
    """
    url = reverse('news:detail', args=news_pk)
    response = author_client.post(url, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    comment_count = Comment.objects.count()
    assert comment_count == 0
