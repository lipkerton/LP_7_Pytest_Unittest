from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('anonymous'), HTTPStatus.FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        
    ),
)
@pytest.mark.parametrize(
    'name, args, args_comment',
    (
        ('news:home', False, False),
        ('news:detail', True, False),
        ('users:login', False, False),
        ('users:logout', False, False),
        ('users:signup', False, False),
        ('news:edit', False, True),
        ('news:delete', False, True),
    ),
)
def test_pages_availability_for_different_users(
    name, news, args, args_comment, comment, expected_status, parametrized_client
):
    url = reverse(
        name, args=((comment.id,) if args_comment else (news.id,) if args else None)
    )
    response = parametrized_client.get(url)
    assert response.status_code == (expected_status if args_comment else HTTPStatus.OK)


@pytest.mark.parametrize(
    'name',
    (
        'news:edit',
        'news:delete',
    ),
)
def test_redirects(client, name, comment):
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
