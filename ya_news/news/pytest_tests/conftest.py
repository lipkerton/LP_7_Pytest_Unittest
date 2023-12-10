from datetime import timedelta

import pytest
from django.conf import settings
from django.test import Client
from django.utils import timezone

from news.models import Comment, News

today = timezone.now()


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def anonymous(client):
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
    return news


@pytest.fixture
def all_news():
    News.objects.bulk_create(
        [
            News(
                title=f'Новость {index}',
                text='Просто текст',
                date=today - timedelta(days=index),
            ) for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        ]
    )


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Привет',
    )
    return comment


@pytest.fixture
def all_comments(author, news):
    for index in range(2):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = today - timedelta(days=index)
        comment.save()
