from django.contrib.auth.models import User
from django.http import QueryDict
from django.test import override_settings
from django.urls import reverse

from sample_app.models import PersonFactory
from tests.conftest import PersonAC


def urls():
    p = PersonFactory()

    toggle_url = reverse(
        "autocomplete:toggle",
        kwargs={
            "ac_name": "PersonAC",
        },
    )

    qs_dict = QueryDict(mutable=True)
    qs_dict.update(
        {
            "field_name": "myfield_name",
            "item": p.id,
        },
    )
    toggle_url = f"{toggle_url}?{qs_dict.urlencode()}"

    items_url = reverse(
        "autocomplete:items",
        kwargs={
            "ac_name": "PersonAC",
        },
    )

    qs_dict = QueryDict(mutable=True)
    qs_dict.update(
        {
            "field_name": "myfield_name",
            "component_prefix": "component_name",
            "search": "abcd",
        },
    )
    items_url = f"{items_url}?{qs_dict.urlencode()}"

    return toggle_url, items_url


def test_auth_check_blocks_unauthenticated(client):

    with override_settings(AUTOCOMPLETE_BLOCK_UNAUTHENTICATED=True):
        response = client.get(urls()[0])
        assert response.status_code == 403
        response = client.get(urls()[1])
        assert response.status_code == 403


def test_disabled_auth_check_allows_unauthenticated(client):
    with override_settings(AUTOCOMPLETE_BLOCK_UNAUTHENTICATED=False):
        response = client.get(urls()[0])
        assert response.status_code == 200
        response = client.get(urls()[1])
        assert response.status_code == 200


def test_auth_check_enabled_allows_authenticated(client):
    u = User.objects.create(username="a")
    client.force_login(u)

    with override_settings(AUTOCOMPLETE_BLOCK_UNAUTHENTICATED=True):
        response = client.get(urls()[0])
        assert response.status_code == 200
        response = client.get(urls()[1])
        assert response.status_code == 200
