import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(client, news_home, all_news):
    url = news_home
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_home):
    url = news_home
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, news, news_detail, all_comments):
    url = news_detail
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = [comment.created for comment in news.comment_set.all()]
    sorted_comments = sorted(all_comments)
    assert all_comments == sorted_comments


def test_anonymous_client_has_no_form(client, news_detail):
    url = news_detail
    response = client.get(url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, news_detail):
    url = news_detail
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
