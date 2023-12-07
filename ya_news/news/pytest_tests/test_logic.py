from news.models import Comment
from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects, assertFormError
from news.forms import BAD_WORDS, WARNING
from http import HTTPStatus


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, id_news, form_data):
    url = reverse('news:detail', args=id_news)
    client.post(url, data=form_data)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_can_create_comment(
    id_news, admin_client, admin_user, news, form_data
):
    url = reverse('news:detail', args=id_news)
    response = admin_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == admin_user


def test_user_cant_use_bad_words(admin_client, id_news):
    url = reverse('news:detail', args=id_news)
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


def test_author_can_delete_comment(author_client, id_news, id_comment):
    news_url = reverse('news:detail', args=id_news)
    url_to_comments = news_url + '#comments'
    delete_url = reverse('news:delete', args=id_comment)
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(admin_client, id_comment):
    delete_url = reverse('news:delete', args=id_comment)
    response = admin_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(author_client, id_news, comment, form_data):
    news_url = reverse('news:detail', args=id_news)
    url_to_comments = news_url + '#comments'
    edit_url = reverse('news:edit', args=(comment.id,))
    response = author_client.post(edit_url, data=form_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_user_cant_edit_comment_of_another_user(
    admin_client, comment, form_data
):
    edit_url = reverse('news:edit', args=(comment.id,))
    response = admin_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == 'Привет'
