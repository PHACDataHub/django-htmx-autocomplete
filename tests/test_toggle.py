from django.urls import reverse

from sample_app.models import Person, PersonFactory, Team, TeamFactory

from .utils_for_test import get_soup, put_request_as_querystring


def test_toggle_multi_response(client):
    """
    Scenario: you have a multi-field that may have data,
    you want to add or  remove new item to the field
    clicking the chips fires off these requests,
    so does clicking a search option
    the response is swapped in and replaces the existing chips
    """

    team = TeamFactory()
    people = PersonFactory.create_batch(5)
    stable_member = PersonFactory(name="abcdefg")
    member_to_remove = PersonFactory(name="abcdefg2")
    member_to_add = PersonFactory(name="abcdxyz")
    # team.members.add(stable_member)
    # team.members.add(member_to_remove)

    url = reverse("members_ac", kwargs={"method": "toggle"})

    # toggle member_to_add ON
    data = {
        "members_ac": [stable_member.id, member_to_remove.id],
        "name": "members_ac",  # note: this NEEDS to match the name on the AC view class
        "item": member_to_add.id,
        "component_id": "component_name",
    }

    response = put_request_as_querystring(
        client,
        url,
        data=data,
    )
    assert response.status_code == 200

    soup = get_soup(response)

    # 1. The element we are toggling
    # not sure why this is even included, it doesn't seem to get swapped anywhere
    # I guess we need something?
    toggled_option = soup.select("a[role='option']")
    assert len(toggled_option) == 1

    # 2. The hidden inputs that actually hold the form values
    hidden_inputs_container = soup.select_one("div#component_name")
    assert hidden_inputs_container.attrs["hx-swap-oob"] == "true"
    hidden_inputs = hidden_inputs_container.select(
        "input[type='hidden'][name='members_ac']"
    )
    assert len(hidden_inputs) == 3
    values = {int(i.attrs["value"]) for i in hidden_inputs}
    assert values == {stable_member.id, member_to_remove.id, member_to_add.id}

    # 3. The autocomplete 'component', containing chips and fresh text-input
    assert soup.select_one("ul#component_name_ac_container")
    chips = soup.select("ul#component_name_ac_container > li.chip")
    input_li = soup.select("ul#component_name_ac_container > li.input:not(.chip)")
    assert len(chips) == 3
    assert len(input_li) == 1

    # 4. The "info", I think this is a11y stuff
    info_text = soup.select_one("div#component_name__info").get_text()
    assert stable_member.name in info_text
    assert member_to_remove.name in info_text
    assert member_to_add.name in info_text

    # 5. screen reader description, kinda redundant with 4
    sr_description = soup.select_one("div#component_name__sr_description").get_text()
    assert stable_member.name in sr_description
    assert member_to_remove.name in sr_description
    assert member_to_add.name in sr_description

    #
    # now try again, removing a member this time
    # wont check everything again, just that the items seem correct

    data = {
        "members_ac": [stable_member.id, member_to_remove.id],
        "name": "members_ac",  # note: this NEEDS to match the name on the AC view class
        "item": member_to_remove.id,
        "component_id": "component_name",
    }

    response = put_request_as_querystring(
        client,
        url,
        data=data,
    )
    assert response.status_code == 200

    soup = get_soup(response)

    hidden_inputs_container = soup.select_one("div#component_name")
    hidden_inputs = hidden_inputs_container.select(
        "input[type='hidden'][name='members_ac']"
    )
    assert len(hidden_inputs) == 1
    assert hidden_inputs[0].attrs["value"] == str(stable_member.id)

    # another edge case, try remove a member when there's only one left
    data = {
        "members_ac": [member_to_remove.id],
        "name": "members_ac",  # note: this NEEDS to match the name on the AC view class
        "item": member_to_remove.id,
        "component_id": "component_name",
    }

    response = put_request_as_querystring(
        client,
        url,
        data=data,
    )
    assert response.status_code == 200
    soup = get_soup(response)

    hidden_inputs_container = soup.select_one("div#component_name")
    hidden_inputs = hidden_inputs_container.select(
        "input[type='hidden'][name='members_ac']"
    )
    assert len(hidden_inputs) == 0

    # also, another edge case, adding the first member,
    data = {
        "members_ac": [],
        "name": "members_ac",  # note: this NEEDS to match the name on the AC view class
        "item": member_to_add.id,
        "component_id": "component_name",
    }

    response = put_request_as_querystring(
        client,
        url,
        data=data,
    )
    assert response.status_code == 200
    soup = get_soup(response)

    hidden_inputs_container = soup.select_one("div#component_name")
    hidden_inputs = hidden_inputs_container.select(
        "input[type='hidden'][name='members_ac']"
    )
    assert len(hidden_inputs) == 1


def test_toggle_on_non_multi_response(client):
    """
    same as above, but with non-multi field
    """

    team = TeamFactory()
    member1 = PersonFactory(name="abcdefg")
    member2 = PersonFactory(name="xyzijk")

    url = reverse("team_lead_ac", kwargs={"method": "toggle"})

    data = {
        # "team_lead_ac": None,
        "name": "team_lead_ac",  # note this needs to match the name on the AC view class
        "item": member2.id,
        "component_id": "component_name",
    }

    response = put_request_as_querystring(
        client,
        url,
        data,
    )
    assert response.status_code == 200
    soup = get_soup(response)

    # check for all of the parts,

    # 1. The element we are toggling (not sure why this is even included)
    toggled_option = soup.select("a[role='option']")
    assert len(toggled_option) == 1

    # 2. The hidden inputs that actually hold the form values
    hidden_inputs_container = soup.select_one("div#component_name")
    assert hidden_inputs_container.attrs["hx-swap-oob"] == "true"
    hidden_inputs = hidden_inputs_container.select(
        "input[type='hidden'][name='team_lead_ac']"
    )
    assert len(hidden_inputs) == 1
    assert hidden_inputs[0].attrs["value"] == str(member2.id)

    # 3. The autocomplete input
    # this component should have mostly been tested in the items test
    text_input = soup.select_one("input#component_name__textinput")
    assert text_input.attrs["value"] == member2.name

    # 4. The "data" span, not sure how this is used
    data_span = soup.select_one("span#component_name__data")
    assert data_span.attrs["data-phac-aspc-autocomplete"] == str(member2.name)

    # 5. some script tag to keep events updated,
    script_tag = soup.select_one("script[data-componentid='component_name']")
    assert "phac_aspc_autocomplete_trigger_change" in script_tag.get_text()


def test_toggle_off_non_multi_response(client):
    """
    same as above, but toggling off
    not checking as much stuff
    """

    team = TeamFactory()
    member1 = PersonFactory(name="abcdefg")
    member2 = PersonFactory(name="xyzijk")

    url = reverse("team_lead_ac", kwargs={"method": "toggle"})

    # try un-toggling the member
    data = {
        "team_lead_ac": member2.id,
        "name": "team_lead_ac",  # note this needs to match the name on the AC view class
        "item": member2.id,
        "component_id": "component_name",
    }

    response = put_request_as_querystring(
        client,
        url,
        data,
    )
    assert response.status_code == 200
    soup = get_soup(response)

    # because this field is not "required", the hidden-input should be removed
    hidden_input = soup.select_one("div#component_name")
    assert hidden_input.get_text().strip() == ""

    text_input = soup.select_one("input#component_name__textinput")
    assert "value" not in text_input.attrs

    data_span = soup.select_one("span#component_name__data")
    assert data_span.attrs["data-phac-aspc-autocomplete"] == ""
