from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args, user, status',
    (
        (
            'news:home',
            None,
            pytest.lazy_fixture('admin_client'),
            HTTPStatus.OK
        ),
        (
            'news:detail',
            pytest.lazy_fixture('news'),
            pytest.lazy_fixture('admin_client'),
            HTTPStatus.OK
        ),
        (
            'users:login',
            None,
            pytest.lazy_fixture('admin_client'),
            HTTPStatus.OK
        ),
        (
            'users:logout',
            None,
            pytest.lazy_fixture('admin_client'),
            HTTPStatus.OK
        ),
        (
            'users:signup',
            None,
            pytest.lazy_fixture('admin_client'),
            HTTPStatus.OK
        ),
        (
            'news:edit',
            pytest.lazy_fixture('comment'),
            pytest.lazy_fixture('admin_client'),
            HTTPStatus.NOT_FOUND
        ),
        (
            'news:delete',
            pytest.lazy_fixture('comment'),
            pytest.lazy_fixture('admin_client'),
            HTTPStatus.NOT_FOUND
        ),
        (
            'news:home',
            None,
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
        (
            'news:detail',
            pytest.lazy_fixture('news'),
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
        (
            'users:login',
            None,
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
        (
            'users:logout',
            None,
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
        (
            'users:signup',
            None,
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
        (
            'news:edit',
            pytest.lazy_fixture('comment'),
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
        (
            'news:delete',
            pytest.lazy_fixture('comment'),
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
        (
            'news:home',
            None,
            pytest.lazy_fixture('anonymous'),
            HTTPStatus.OK
        ),
        (
            'news:detail',
            pytest.lazy_fixture('news'),
            pytest.lazy_fixture('anonymous'),
            HTTPStatus.OK
        ),
        (
            'users:login',
            None,
            pytest.lazy_fixture('anonymous'),
            HTTPStatus.OK
        ),
        (
            'users:logout',
            None,
            pytest.lazy_fixture('anonymous'),
            HTTPStatus.OK
        ),
        (
            'users:signup',
            None,
            pytest.lazy_fixture('anonymous'),
            HTTPStatus.OK
        ),
        (
            'news:edit',
            pytest.lazy_fixture('comment'),
            pytest.lazy_fixture('anonymous'),
            HTTPStatus.FOUND
        ),
        (
            'news:delete',
            pytest.lazy_fixture('comment'),
            pytest.lazy_fixture('anonymous'),
            HTTPStatus.FOUND
        ),
    ),
)
def test_pages_availability_for_different_users(
    name,
    args,
    user,
    status
):
    if args is not None:
        url = reverse(name, args=(args.id,))
    else:
        url = reverse(name)
    response = user.get(url)
    assert response.status_code == status


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
