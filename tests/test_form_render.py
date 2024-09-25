import pytest
from django.urls import reverse

from sample_app.models import Person, PersonFactory, Team, TeamFactory

from .utils_for_test import get_soup


def test_render_widgets_from_form(client):
    url = reverse("index")
    response = client.get(url)
    assert response.status_code == 200


def test_form_non_multi_with_no_data(client):
    team = TeamFactory(team_lead=None)
    people = PersonFactory.create_batch(5)

    assert team.team_lead is None

    url = reverse("edit_team", args=[team.id])
    response = client.get(url)
    assert response.status_code == 200

    soup = get_soup(response)
    team_lead_container = soup.select_one(".team_lead-field-container")

    scripts = team_lead_container.select("script")
    assert len(scripts) == 1
    script = scripts[0]
    assert script.attrs["data-componentid"] == "team_lead_ac"
    assert script.attrs["data-toggleurl"] == "/ac/team_lead_ac/toggle"

    inputs = team_lead_container.select("#team_lead_ac input")
    assert len(inputs) == 1
    input = inputs[0]
    assert input["type"] == "hidden"
    assert "value" not in input.attrs
    assert input.attrs["name"] == "team_lead_ac"

    ul = team_lead_container.select_one("ul#team_lead_ac_ac_container.ac_container")
    assert ul

    data_span = team_lead_container.select_one("span#team_lead_ac__data")
    assert "data-phac-aspc-autocomplete" not in data_span.attrs

    actual_input_field = ul.select_one("li > input")
    assert actual_input_field.attrs["type"] == "text"
    assert "name" not in actual_input_field.attrs
    assert actual_input_field.attrs["aria-controls"] == "team_lead_ac__items"
    assert actual_input_field.attrs["hx-get"] == "/ac/team_lead_ac/items"
    assert actual_input_field.attrs["hx-include"] == "#team_lead_ac"
    assert actual_input_field.attrs["hx-target"] == "#team_lead_ac__items"
    assert (
        "getElementById('team_lead_ac__textinput')"
        in actual_input_field.attrs["hx-vals"]
    )
    assert "name: 'team_lead_ac', " in actual_input_field.attrs["hx-vals"]
    assert "component_id: 'team_lead_ac', " in actual_input_field.attrs["hx-vals"]
    assert "value" not in actual_input_field.attrs


def test_form_non_multi_with_existing_data(client):
    team = TeamFactory()
    people = PersonFactory.create_batch(5)

    team.members.set(people[:2])
    team.team_lead = people[0]
    team.save()

    url = reverse("edit_team", args=[team.id])
    response = client.get(url)
    assert response.status_code == 200

    soup = get_soup(response)

    team_lead_container = soup.select_one(".team_lead-field-container")

    hidden_input = team_lead_container.select_one("#team_lead_ac input")
    assert hidden_input.attrs["value"] == str(people[0].id)
    assert hidden_input.attrs["name"] == "team_lead_ac"

    data_span = team_lead_container.select_one("span#team_lead_ac__data")
    assert data_span.attrs["data-phac-aspc-autocomplete"] == people[0].name

    actual_input_field = team_lead_container.select_one("ul.ac_container li > input")
    assert actual_input_field.attrs["value"] == people[0].name


def test_form_multi_with_no_data(client):
    team = TeamFactory(team_lead=None)
    people = PersonFactory.create_batch(5)

    assert team.team_lead is None

    url = reverse("edit_team", args=[team.id])
    response = client.get(url)
    assert response.status_code == 200

    soup = get_soup(response)

    members_container = soup.select_one(".members-field-container")

    scripts = members_container.select("script")
    assert len(scripts) == 1
    script = scripts[0]
    assert script.attrs["data-componentid"] == "members_ac"
    assert script.attrs["data-toggleurl"] == "/ac/members_ac/toggle"

    data_span = members_container.select_one("span#members_ac__data")
    assert "data-phac-aspc-autocomplete" not in data_span.attrs

    ul = members_container.select_one("ul#members_ac_ac_container.ac_container")
    assert ul

    actual_input_field = ul.select_one("li > input")
    assert actual_input_field.attrs["type"] == "text"
    assert "name" not in actual_input_field.attrs
    assert actual_input_field.attrs["aria-controls"] == "members_ac__items"
    assert actual_input_field.attrs["hx-get"] == "/ac/members_ac/items"
    assert actual_input_field.attrs["hx-include"] == "#members_ac"
    assert actual_input_field.attrs["hx-target"] == "#members_ac__items"
    assert "members_ac__textinput" in actual_input_field.attrs["hx-vals"]
    assert "value" not in actual_input_field.attrs


def test_form_multi_with_data(client):
    team = TeamFactory(team_lead=None)
    people = PersonFactory.create_batch(5)

    members = people[:2]
    team.members.set(members)

    url = reverse("edit_team", args=[team.id])
    response = client.get(url)
    assert response.status_code == 200

    soup = get_soup(response)

    members_container = soup.select_one(".members-field-container")

    hidden_inputs = members_container.select("#members_ac input")
    member_ids = set()
    for input in hidden_inputs:
        assert input.attrs["type"] == "hidden"
        assert input.attrs["name"] == "members_ac"
        member_ids.add(int(input.attrs["value"]))

    assert member_ids == {members[0].id, members[1].id}

    data_span = members_container.select_one("span#members_ac__data")
    assert "data-phac-aspc-autocomplete" not in data_span.attrs

    # now look at the autocomplete input and its chip siblings,
    ac_items = list(
        members_container.select("ul#members_ac_ac_container.ac_container > li.chip")
    )
    assert len(ac_items) == 2
    for li in ac_items:
        assert li.select_one("span").text in {members[0].name, members[1].name}
        delete_button = li.select_one("a")
        assert delete_button.attrs["hx-put"] == "/ac/members_ac/toggle"
        assert (
            delete_button.attrs["hx-params"]
            == "members_ac,name,item,remove,component_id"
        )
        assert delete_button.attrs["hx-vals"]
        assert delete_button.attrs["hx-include"] == "#members_ac"
        assert delete_button.attrs["hx-swap"] == "delete"
        assert delete_button.attrs["hx-target"] == "this"
        assert delete_button.attrs["href"] == "#"

    input_li = list(
        members_container.select(
            "ul#members_ac_ac_container.ac_container > li:not(.chip).input"
        )
    )
    assert len(input_li) == 1
    input_li = input_li[0]
    input_field = input_li.select_one("input")
    assert input_field.attrs["type"] == "text"
    assert "name" not in input_field.attrs
    assert input_field.attrs["aria-controls"] == "members_ac__items"
    assert input_field.attrs["hx-get"] == "/ac/members_ac/items"
    assert input_field.attrs["hx-include"] == "#members_ac"
    assert input_field.attrs["hx-target"] == "#members_ac__items"
    assert "getElementById('members_ac__textinput')" in input_field.attrs["hx-vals"]
    assert "name: 'members_ac', " in input_field.attrs["hx-vals"]
    assert "component_id: 'members_ac', " in input_field.attrs["hx-vals"]
    assert "value" not in input_field.attrs
