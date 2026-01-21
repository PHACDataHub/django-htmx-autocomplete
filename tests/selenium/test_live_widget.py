from django.urls import reverse

import pytest

from sample_app.models import Person, PersonFactory, Team, TeamFactory

from .selenium_util import (
    click_button,
    get_element,
    get_elements,
    wait_until_selector,
    wait_until_selector_gone,
)

# tag the whole module
pytestmark = [
    pytest.mark.selenium,
    pytest.mark.django_db(transaction=True),
]


def test_single_select_live_widget(live_server, driver):
    p1 = PersonFactory(name="Sample Leader")
    p2 = PersonFactory(name="Sample Member 2")
    p3 = PersonFactory(name="Sample Member 3")
    t1 = TeamFactory(team_lead=p1)

    url = reverse("edit_team", args=[t1.pk])

    driver.get(live_server.url + url)

    def get_info_txt():
        info = get_element(driver, "#team_lead__info")
        return info.get_attribute("innerHTML").replace("\n", " ")

    listbox = get_element(driver, "div[role='listbox']")
    assert not listbox.get_attribute("innerHTML")

    click_button(driver, "input#team_lead__textinput")

    listbox = get_element(driver, "div[role='listbox']")

    assert "1 result available" in get_info_txt()

    assert listbox.is_displayed()
    html = listbox.get_attribute("outerHTML")

    options = listbox.find_elements("css selector", "a[role='option']")
    assert len(options) == 1

    # click the option to un-select it
    click_button(driver, "a[role='option']")

    assert "Nothing selected" in get_info_txt()

    # activate the list box again by clicking the input
    click_button(driver, "input#team_lead__textinput")

    option = get_element(driver, "div[role='listbox'] span.item")
    assert "Type at least" in option.get_attribute("outerHTML")

    assert "Type at least" in get_info_txt()

    input = get_element(driver, "input#team_lead__textinput")
    input.send_keys("Sample")

    wait_until_selector(driver, "div[role='listbox'] a[role='option']")

    options = get_elements(driver, "div[role='listbox'] a[role='option']")

    assert len(options) == 3

    assert "3 results available" in get_info_txt()

    click_button(driver, "a[role='option']")
    assert "Sample" in get_info_txt()
    assert "selected" in get_info_txt()

    # now check that the selected option is in the input box
    input = get_element(driver, "input#team_lead__textinput")
    assert input.get_attribute("value") == "Sample Leader"

    # and that the invisible input has the correct value
    hidden_input = get_element(driver, "input[name='team_lead']")
    assert hidden_input.get_attribute("value") == str(p1.pk)


def test_multi_select_live_widget(live_server, driver):
    p1 = PersonFactory(name="Sample Member 1")
    p2 = PersonFactory(name="Sample Member 2")
    p3 = PersonFactory(name="Sample Member 3")
    p4 = PersonFactory(name="Sample Member 4")
    p4 = PersonFactory(name="Sample Member 5")
    t1 = TeamFactory(team_lead=p1)
    t1.members.set([p1, p2])

    url = reverse("edit_team", args=[t1.pk])

    driver.get(live_server.url + url)

    def get_sr_text():
        info = get_element(driver, "#members__sr_description")
        return info.get_attribute("innerHTML").replace("\n", " ")

    sr_text = get_sr_text()
    assert "2  selected." in sr_text
    assert "Sample Member 1 selected," in sr_text
    assert "Sample Member 2 selected," in sr_text
    assert "Press backspace to delete the last selected item." in sr_text

    # add a member - click the input box
    click_button(driver, "input#members__textinput")

    wait_until_selector(driver, "div[role='listbox'].show")

    sr_text = get_sr_text()
    assert "Sample member 1 selected,"
    assert "Sample Member 2 selected," in sr_text
    assert "Press backspace to delete the last selected item." in sr_text

    listbox = get_element(driver, "#members__container div[role='listbox']")
    assert listbox.is_displayed()
    options = listbox.find_elements(
        "css selector",
        "#members__container a[role='option'][aria-selected='true']",
    )
    # although options require ≥ 3 characters to search, selected options are already shown
    assert len(options) == 2

    # unselect the first option
    click_button(driver, "#members__container a[role='option']")

    wait_until_selector_gone(
        driver, "div#members__container li.chip:nth-child(2)"
    )

    sr_text = get_sr_text()
    assert "1  selected." in sr_text

    # check the chips and hidden inputs are both updated
    chips = get_elements(driver, "div#members__container li.chip")
    assert len(chips) == 1
    hidden_inputs = get_elements(driver, "input[name='members']")
    assert len(hidden_inputs) == 1

    # unselect the other option, this time with the chip button
    # click the 'x' button on the chip
    click_button(driver, "div#members__container li.chip a")

    wait_until_selector_gone(driver, "div#members__container li.chip")

    # now nothing should be selected
    chips = get_elements(driver, "div#members__container li.chip")
    assert len(chips) == 0

    hidden_inputs = get_elements(
        driver, "#members__container input[name='members']"
    )
    assert len(hidden_inputs) == 1
    assert not hidden_inputs[0].get_attribute("value")

    assert "" == get_sr_text().strip()
