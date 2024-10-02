import pytest
from django import forms
from django.template import Context, Template, loader
from django.urls import reverse

from autocomplete import Autocomplete, AutocompleteWidget, ModelAutocomplete, register
from sample_app.models import Person, PersonFactory, Team, TeamFactory

from .utils_for_test import soup_from_str


class PersonModelAC(ModelAutocomplete):
    model = Person
    search_attrs = ["name"]


def test_model_ac_search():
    p1 = PersonFactory(name="John1")
    p2 = PersonFactory(name="John2")
    p3 = PersonFactory(name="John3")
    p4 = PersonFactory(name="Jones")

    results = PersonModelAC.search_items("Joh", {})

    assert len(results) == 3
    assert results == [
        {"label": "John1", "key": p1.id},
        {"label": "John2", "key": p2.id},
        {"label": "John3", "key": p3.id},
    ]

    assert PersonModelAC.get_items_from_keys([p1.id, p2.id], {}) == [
        {"label": "John1", "key": p1.id},
        {"label": "John2", "key": p2.id},
    ]
