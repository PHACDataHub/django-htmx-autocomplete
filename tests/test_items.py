import json

from django.http import QueryDict
from django.urls import reverse

from sample_app.models import Person, PersonFactory, Team, TeamFactory

from .utils_for_test import get_soup


def test_items_response_multi(client):
    """
    Scenario: you have a multi-field that already has data.
    You are searching for a new item,
    the search fires off a request for new items
    """

    team = TeamFactory()
    people = PersonFactory.create_batch(5)
    searchable_person = PersonFactory(name="abcdefg")
    searchable_person2 = PersonFactory(name="abcdxyz")

    base_url = reverse("members_ac", kwargs={"method": "items"})

    qs_dict = QueryDict(mutable=True)
    qs_dict.setlist("members_ac", [])
    qs_dict.update(
        {
            "name": "field_name",
            "component_id": "component_name",
            "search": "abcd",
        }
    )
    full_url = f"{base_url}?{qs_dict.urlencode()}"

    response = client.get(full_url)
    assert response.status_code == 200

    soup = get_soup(response)

    listbox = soup.select_one("div[role='listbox']")
    assert listbox.attrs["id"] == "component_name__items"
    assert listbox.attrs["aria-multiselectable"] == "true"
    assert listbox.attrs["aria-description"] == "multiselect"

    # abcd should match two people,
    options = listbox.select("a")
    assert len(options) == 2
    assert "abcdefg" in options[0].get_text()
    assert "abcdxyz" in options[1].get_text()

    assert json.loads(options[0].attrs["hx-vals"]) == {
        "name": "field_name",
        "component_id": "component_name",
        "item": str(searchable_person.id),
    }
    assert json.loads(options[1].attrs["hx-vals"]) == {
        "name": "field_name",
        "component_id": "component_name",
        "item": str(searchable_person2.id),
    }

    highlight_span = listbox.select_one("span.highlight")
    assert highlight_span.get_text() == "abcd"

    assert options[0].attrs["hx-put"] == reverse(
        "members_ac", kwargs={"method": "toggle"}
    )
    assert options[0].attrs["hx-params"] == "field_name,name,item,component_id"
    assert options[0].attrs["hx-include"] == "#component_name"
    assert "component_name__item__" in options[0].attrs["id"]
    assert not options[1].attrs["id"] == options[0].attrs["id"]

    # now add abcdefg as member and try again,
    qs_dict.setlist("members_ac", [searchable_person.id])
    full_url = f"{base_url}?{qs_dict.urlencode()}"

    response = client.get(full_url)
    assert response.status_code == 200

    soup = get_soup(response)

    options = soup.select("div[role='listbox'] > a")
    assert len(options) == 2
    assert "abcdefg" in options[0].get_text()
    assert "abcdxyz" in options[1].get_text()

    assert options[0].attrs["aria-selected"] == "true"


def test_items_response_single(client):
    """
    Scenario: same as above, but with a non-multi field
    """

    team = TeamFactory()
    people = PersonFactory.create_batch(5)
    searchable_person = PersonFactory(name="abcdefg")
    searchable_person2 = PersonFactory(name="abcdxyz")

    base_url = reverse("team_lead_ac", kwargs={"method": "items"})

    qs_dict = QueryDict(mutable=True)
    qs_dict.update(
        {
            "name": "field_name",
            "component_id": "component_name",
            "search": "abcd",
        }
    )
    full_url = f"{base_url}?{qs_dict.urlencode()}"

    response = client.get(full_url)
    assert response.status_code == 200

    soup = get_soup(response)

    listbox = soup.select_one("div[role='listbox']")
    assert listbox.attrs["id"] == "component_name__items"
    assert "aria-multiselectable" not in listbox.attrs

    # abcd should match two people,
    options = listbox.select("a")
    assert len(options) == 2
    assert "abcdefg" in options[0].get_text()
    assert "abcdxyz" in options[1].get_text()

    assert json.loads(options[0].attrs["hx-vals"]) == {
        "name": "field_name",
        "component_id": "component_name",
        "item": str(searchable_person.id),
    }
    assert json.loads(options[1].attrs["hx-vals"]) == {
        "name": "field_name",
        "component_id": "component_name",
        "item": str(searchable_person2.id),
    }

    highlight_span = listbox.select_one("span.highlight")
    assert highlight_span.get_text() == "abcd"

    assert options[0].attrs["hx-put"] == reverse(
        "team_lead_ac", kwargs={"method": "toggle"}
    )
    assert options[0].attrs["hx-params"] == "field_name,name,item,component_id"
    assert options[0].attrs["hx-include"] == "#component_name"
    assert "component_name__item__" in options[0].attrs["id"]
    assert not options[1].attrs["id"] == options[0].attrs["id"]

    qs_dict["team_lead_ac"] = searchable_person.id
    full_url = f"{base_url}?{qs_dict.urlencode()}"

    response = client.get(full_url)
    assert response.status_code == 200

    soup = get_soup(response)

    options = soup.select("div[role='listbox'] > a")
    assert len(options) == 2
    assert "abcdefg" in options[0].get_text()
    assert "abcdxyz" in options[1].get_text()

    assert options[0].attrs["aria-selected"] == "true"
