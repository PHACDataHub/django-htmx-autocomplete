import pytest
from django.db import transaction

from autocomplete import Autocomplete, ModelAutocomplete, register
from sample_app.models import Person


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    without this, tests (including old-style) have to explicitly declare db as a dependency
    https://pytest-django.readthedocs.io/en/latest/faq.html#how-can-i-give-database-access-to-all-my-tests-without-the-django-db-marker
    """
    pass


@pytest.fixture(scope="session")
def globally_scoped_fixture_helper(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        # Wrap in try + atomic block to do non crashing rollback
        # This means we don't have to re-create a test DB each time
        try:
            with transaction.atomic():
                yield
                raise Exception
        except Exception:
            pass


@register
class PersonAC(ModelAutocomplete):
    model = Person
    search_attrs = ["name"]
