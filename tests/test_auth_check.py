from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import QueryDict
from django.test import override_settings
from django.urls import reverse

from autocomplete import ModelAutocomplete, register
from sample_app.models import Person, PersonFactory
from tests.conftest import PersonAC


def urls(ac_name="PersonAC"):
    p = PersonFactory()

    toggle_url = reverse(
        "autocomplete:toggle",
        kwargs={
            "ac_name": ac_name,
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
            "ac_name": ac_name,
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


@register
class SinglePermAC(ModelAutocomplete):
    model = Person
    search_attrs = ["name"]
    permission_required = "sample_app.view_person"


@register
class MultiPermAC(ModelAutocomplete):
    model = Person
    search_attrs = ["name"]
    permission_required = ["sample_app.view_person", "sample_app.change_person"]


@register
class NoPermAC(ModelAutocomplete):
    model = Person
    search_attrs = ["name"]
    permission_required = None


def test_no_permission_required_allows_any_authenticated_user(client):
    u = User.objects.create(username="no_perm_user")
    client.force_login(u)

    toggle_url, items_url = urls("NoPermAC")
    assert client.get(toggle_url).status_code == 200
    assert client.get(items_url).status_code == 200


def test_no_permission_required_allows_unauthenticated(client):
    toggle_url, items_url = urls("NoPermAC")
    assert client.get(toggle_url).status_code == 200
    assert client.get(items_url).status_code == 200


def test_single_permission_blocks_unauthenticated(client):
    toggle_url, items_url = urls("SinglePermAC")
    assert client.get(toggle_url).status_code == 403
    assert client.get(items_url).status_code == 403


def test_single_permission_blocks_user_without_perm(client):
    u = User.objects.create(username="no_perm")
    client.force_login(u)

    toggle_url, items_url = urls("SinglePermAC")
    assert client.get(toggle_url).status_code == 403
    assert client.get(items_url).status_code == 403


def test_single_permission_allows_user_with_perm(client):
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType

    ct = ContentType.objects.get(app_label="sample_app", model="person")
    u = User.objects.create(username="has_perm")
    u.user_permissions.add(
        Permission.objects.get(content_type=ct, codename="view_person")
    )
    client.force_login(u)

    toggle_url, items_url = urls("SinglePermAC")
    assert client.get(toggle_url).status_code == 200
    assert client.get(items_url).status_code == 200


def test_multi_permission_blocks_user_with_partial_perms(client):
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType

    ct = ContentType.objects.get(app_label="sample_app", model="person")
    u = User.objects.create(username="partial_perm")
    u.user_permissions.add(
        Permission.objects.get(content_type=ct, codename="view_person")
    )
    client.force_login(u)

    toggle_url, items_url = urls("MultiPermAC")
    assert client.get(toggle_url).status_code == 403
    assert client.get(items_url).status_code == 403


def test_multi_permission_blocks_user_with_no_perms(client):
    u = User.objects.create(username="no_perms_at_all")
    client.force_login(u)

    toggle_url, items_url = urls("MultiPermAC")
    assert client.get(toggle_url).status_code == 403
    assert client.get(items_url).status_code == 403


def test_multi_permission_allows_user_with_all_perms(client):
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType

    ct = ContentType.objects.get(app_label="sample_app", model="person")
    u = User.objects.create(username="all_perms")
    u.user_permissions.add(
        Permission.objects.get(content_type=ct, codename="view_person"),
        Permission.objects.get(content_type=ct, codename="change_person"),
    )
    client.force_login(u)

    toggle_url, items_url = urls("MultiPermAC")
    assert client.get(toggle_url).status_code == 200
    assert client.get(items_url).status_code == 200


def test_auth_check_raises_permission_denied_for_single_perm():
    from unittest.mock import MagicMock

    from django.test import RequestFactory

    rf = RequestFactory()
    request = rf.get("/")
    request.user = MagicMock()
    request.user.is_authenticated = False

    try:
        SinglePermAC.auth_check(request)
    except PermissionDenied as e:
        assert "Authentication required" in str(e)
    else:
        raise AssertionError("PermissionDenied not raised")


def test_auth_check_raises_permission_denied_for_multi_perm():
    from unittest.mock import MagicMock

    from django.test import RequestFactory

    rf = RequestFactory()
    request = rf.get("/")
    request.user = MagicMock()
    request.user.is_authenticated = True
    request.user.has_perms.return_value = False

    try:
        MultiPermAC.auth_check(request)
    except PermissionDenied as e:
        assert "Insufficient permissions" in str(e)
    else:
        raise AssertionError("PermissionDenied not raised")


def test_auth_check_passes_for_user_with_single_perm():
    from unittest.mock import MagicMock

    from django.test import RequestFactory

    rf = RequestFactory()
    request = rf.get("/")
    request.user = MagicMock()
    request.user.is_authenticated = True
    request.user.has_perms.return_value = True

    SinglePermAC.auth_check(request)


def test_auth_check_passes_for_user_with_all_multi_perms():
    from unittest.mock import MagicMock

    from django.test import RequestFactory

    rf = RequestFactory()
    request = rf.get("/")
    request.user = MagicMock()
    request.user.is_authenticated = True
    request.user.has_perms.return_value = True

    MultiPermAC.auth_check(request)


def test_auth_check_passes_when_no_permission_required():
    from unittest.mock import MagicMock

    from django.test import RequestFactory

    rf = RequestFactory()
    request = rf.get("/")
    request.user = MagicMock()
    request.user.is_authenticated = True

    NoPermAC.auth_check(request)


def test_auth_check_unauthenticated_blocked_when_permission_required():
    from unittest.mock import MagicMock

    from django.test import RequestFactory

    rf = RequestFactory()
    request = rf.get("/")
    request.user = MagicMock()
    request.user.is_authenticated = False

    try:
        SinglePermAC.auth_check(request)
    except PermissionDenied as e:
        assert "Authentication required" in str(e)
    else:
        raise AssertionError("PermissionDenied not raised")


def test_auth_check_unauthenticated_blocked_when_multi_permission_required():
    from unittest.mock import MagicMock

    from django.test import RequestFactory

    rf = RequestFactory()
    request = rf.get("/")
    request.user = MagicMock()
    request.user.is_authenticated = False

    try:
        MultiPermAC.auth_check(request)
    except PermissionDenied as e:
        assert "Authentication required" in str(e)
    else:
        raise AssertionError("PermissionDenied not raised")


def test_auth_check_passes_for_unauthenticated_when_no_permission_required():
    from unittest.mock import MagicMock

    from django.test import RequestFactory

    rf = RequestFactory()
    request = rf.get("/")
    request.user = MagicMock()
    request.user.is_authenticated = False

    NoPermAC.auth_check(request)


def test_permission_required_converts_string_to_list():
    from unittest.mock import MagicMock

    from django.test import RequestFactory

    rf = RequestFactory()
    request = rf.get("/")
    request.user = MagicMock()
    request.user.is_authenticated = True
    request.user.has_perms.return_value = True

    SinglePermAC.auth_check(request)

    request.user.has_perms.assert_called_once_with(["sample_app.view_person"])


def test_permission_required_uses_list_directly():
    from unittest.mock import MagicMock

    from django.test import RequestFactory

    rf = RequestFactory()
    request = rf.get("/")
    request.user = MagicMock()
    request.user.is_authenticated = True
    request.user.has_perms.return_value = True

    MultiPermAC.auth_check(request)

    request.user.has_perms.assert_called_once_with(
        ["sample_app.view_person", "sample_app.change_person"]
    )


def test_permission_denied_message_contains_class_name():
    from unittest.mock import MagicMock

    from django.test import RequestFactory

    rf = RequestFactory()
    request = rf.get("/")
    request.user = MagicMock()
    request.user.is_authenticated = True
    request.user.has_perms.return_value = False

    try:
        SinglePermAC.auth_check(request)
    except PermissionDenied as e:
        assert "SinglePermAC" in str(e)
    else:
        raise AssertionError("PermissionDenied not raised")
