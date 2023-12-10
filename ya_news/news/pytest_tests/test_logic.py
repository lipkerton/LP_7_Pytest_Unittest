from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

OLD_FORM_DATA = {'text': 'Привет'}
NEW_FORM_DATA = {'text': 'Новый текст', }
pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(client, news):
    url = reverse('news:detail', args=(news.id,))
    client.post(url, data=NEW_FORM_DATA)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
    admin_client, admin_user, news
):
    url = reverse('news:detail', args=(news.id,))
    response = admin_client.post(url, data=NEW_FORM_DATA)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == NEW_FORM_DATA['text']
    assert comment.news == news
    assert comment.author == admin_user


def test_user_cant_use_bad_words(admin_client, news):
    url = reverse('news:detail', args=(news.id,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = admin_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING,
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client, news, comment):
    news_url = reverse('news:detail', args=(news.id,))
    url_to_comments = f'{news_url}#comments'
    delete_url = reverse('news:delete', args=(comment.id,))
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(admin_client, comment):
    delete_url = reverse('news:delete', args=(comment.id,))
    response = admin_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1
    assert comment.text == OLD_FORM_DATA['text']


def test_author_can_edit_comment(author_client, news, comment):
    news_url = reverse('news:detail', args=(news.id,))
    url_to_comments = f'{news_url}#comments'
    edit_url = reverse('news:edit', args=(comment.id,))
    response = author_client.post(edit_url, data=NEW_FORM_DATA)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == NEW_FORM_DATA['text']


def test_user_cant_edit_comment_of_another_user(
    admin_client, comment
):
    edit_url = reverse('news:edit', args=(comment.id,))
    response = admin_client.post(edit_url, data=NEW_FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == OLD_FORM_DATA['text']
