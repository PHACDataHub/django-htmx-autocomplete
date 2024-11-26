import pytest
from django import forms
from django.template import Context, Template, loader
from django.urls import reverse

from autocomplete import Autocomplete, AutocompleteWidget, register
from sample_app.models import Person, PersonFactory, Team, TeamFactory

from .utils_for_test import soup_from_str


@register
class PersonAC4(Autocomplete):

    @classmethod
    def search_items(cls, search, context):
        qs = Person.objects.filter(name__icontains=search)

        return [{"key": person.id, "label": person.name} for person in qs]

    @classmethod
    def get_items_from_keys(cls, keys, context):
        qs = Person.objects.filter(id__in=keys)
        return [{"key": person.id, "label": person.name} for person in qs]


single_form_template = Template(
    """
        {{ form.as_p }}
    """
)


def render_template(template, ctx_dict):
    context = Context(ctx_dict)
    return template.render(context)


def test_render_widget_in_form_empty():
    class FormWithSingle(forms.ModelForm):
        class Meta:
            model = Team
            fields = ["team_lead"]

            widgets = {
                "team_lead": AutocompleteWidget(
                    ac_class=PersonAC4,
                )
            }

    create_form = FormWithSingle()

    rendered = render_template(single_form_template, {"form": create_form})

    soup = soup_from_str(rendered)

    # check the form label works
    label = soup.select_one("label[for='id_team_lead']")
    assert label.text == "Team lead:"

    # check focus ring,
    focus_ring = soup.select_one("div.phac_aspc_form_autocomplete_focus_ring")
    assert focus_ring

    component_container = focus_ring.select_one(
        "div.phac_aspc_form_autocomplete#team_lead__container"
    )
    assert component_container

    # 1. hidden input are in #<component_id>
    # it starts out empty without even a name
    component = component_container.select_one("#team_lead")
    inputs = component.select('span > input[type="hidden"]')
    assert len(inputs) == 1
    assert inputs[0].attrs["name"] == "team_lead"
    assert "value" not in inputs[0].attrs

    # 2. script
    scripts = soup.select("script")
    assert len(scripts) == 1
    assert scripts[0].attrs["data-componentid"] == "team_lead"
    assert scripts[0].attrs["data-toggleurl"] == reverse(
        "autocomplete:toggle", args=["PersonAC4"]
    )

    ac_container_ul = soup.select_one("ul#team_lead_ac_container.ac_container")
    assert ac_container_ul

    lis = ac_container_ul.select("li")
    assert len(lis) == 1
    actual_input_field = lis[0].select_one("input")
    assert actual_input_field.attrs["type"] == "text"
    assert "name" not in actual_input_field.attrs
    assert actual_input_field.attrs["aria-controls"] == "team_lead__items"
    assert actual_input_field.attrs["hx-get"] == reverse(
        "autocomplete:items", args=["PersonAC4"]
    )
    assert actual_input_field.attrs["hx-include"] == "#team_lead"
    assert actual_input_field.attrs["hx-target"] == "#team_lead__items"
    assert (
        'getElementById("team_lead__textinput")' in actual_input_field.attrs["hx-vals"]
    )
    assert '"component_prefix": "",' in actual_input_field.attrs["hx-vals"]
    assert '"field_name": "team_lead",' in actual_input_field.attrs["hx-vals"]
    assert "value" not in actual_input_field.attrs


def test_render_widget_in_form_non_empty():
    class FormWithSingle(forms.ModelForm):
        class Meta:
            model = Team
            fields = ["team_lead"]

            widgets = {
                "team_lead": AutocompleteWidget(
                    ac_class=PersonAC4,
                )
            }

    lead = PersonFactory()
    record = TeamFactory(team_lead=lead)

    create_form = FormWithSingle(
        instance=record,
    )

    rendered = render_template(single_form_template, {"form": create_form})

    soup = soup_from_str(rendered)

    # check input is populated,
    input = soup.select_one("#team_lead  span > input[type='hidden']")
    assert input.attrs["name"] == "team_lead"
    assert input.attrs["value"] == str(lead.id)

    ac_container_ul = soup.select_one("ul#team_lead_ac_container.ac_container")
    assert ac_container_ul

    lis = ac_container_ul.select("li")
    assert len(lis) == 1
    actual_input_field = lis[0].select_one("input")
    assert actual_input_field.attrs["type"] == "text"
    assert actual_input_field.attrs["value"] == lead.name
    assert "multiselect" not in actual_input_field.attrs["hx-vals"]


def test_render_widget_multi_empty():
    class FormWithMulti(forms.ModelForm):
        class Meta:
            model = Team
            fields = ["members"]

            widgets = {
                "members": AutocompleteWidget(
                    ac_class=PersonAC4, options={"multiselect": True}
                )
            }

    people = PersonFactory.create_batch(5)

    create_form = FormWithMulti()

    rendered = render_template(single_form_template, {"form": create_form})

    soup = soup_from_str(rendered)


def test_render_widget_multi_non_empty():

    class FormWithMulti(forms.ModelForm):
        class Meta:
            model = Team
            fields = ["members"]

            widgets = {
                "members": AutocompleteWidget(
                    ac_class=PersonAC4, options={"multiselect": True}
                )
            }

    people = PersonFactory.create_batch(5)
    record = TeamFactory()
    record.members.set(people[:2])

    edit_form = FormWithMulti(instance=record)

    rendered = render_template(single_form_template, {"form": edit_form})

    soup = soup_from_str(rendered)

    component = soup.select_one("#members")
    hidden_inputs = component.select('span > input[type="hidden"]')

    assert len(hidden_inputs) == 2
    assert hidden_inputs[0].attrs["name"] == "members"
    values = {int(i.attrs["value"]) for i in hidden_inputs}
    assert values == {people[0].id, people[1].id}

    # check untoggle buttons,
    ac_items = soup.select("ul#members_ac_container.ac_container > li.chip")
    assert len(ac_items) == 2
    for li in ac_items:
        assert li.select_one("span").text in {people[0].name, people[1].name}
        delete_button = li.select_one("a")
        assert delete_button.attrs["hx-get"] == reverse(
            "autocomplete:toggle", args=["PersonAC4"]
        )
        assert (
            delete_button.attrs["hx-params"]
            == "members,field_name,item,component_prefix,required,multiselect,remove"
        )
        assert "multiselect" in delete_button.attrs["hx-vals"]
        assert delete_button.attrs["hx-vals"]
        assert delete_button.attrs["hx-include"] == "#members"
        assert delete_button.attrs["hx-swap"] == "delete"
        assert delete_button.attrs["hx-target"] == "this"
        assert delete_button.attrs["href"] == "#"


def test_with_formset():
    p1 = PersonFactory()
    p2 = PersonFactory()
    p3 = PersonFactory()
    people = [p1, p2, p3]
    team1 = TeamFactory(team_lead=p1)
    team2 = TeamFactory(team_lead=p2)
    team3 = TeamFactory(team_lead=None)

    class FormWithSingle(forms.ModelForm):
        class Meta:
            model = Team
            fields = ["team_lead"]

            widgets = {
                "team_lead": AutocompleteWidget(
                    ac_class=PersonAC4,
                )
            }

    forms.modelformset_factory(Team, form=FormWithSingle)

    template = Template(
        """
        <div id='empty-form-container'>
        {{ formset.empty_form }}
        </div>
        <div id='management-form'>
        {{ formset.management_form }}
        </div>
        {% for form in formset %}
            <div class="form-container">
            {{ form.as_p }}
            </div>
        {% endfor %}
    """
    )

    formset = forms.modelformset_factory(Team, form=FormWithSingle, extra=0)(
        queryset=Team.objects.all()
    )

    rendered = render_template(template, {"formset": formset})

    soup = soup_from_str(rendered)

    empty_form = soup.select_one("#empty-form-container")
    assert empty_form

    formset_forms = soup.select(".form-container")
    for ix, form in enumerate(formset_forms):
        hidden_input = form.select_one(
            f"input[type='hidden'][name='form-{ix}-team_lead']"
        )
        if ix in (0, 1):
            assert hidden_input.attrs["value"] == str(people[ix].id)
        if ix == 2:
            assert not hidden_input


def test_custom_options():
    class FormWithSingle(forms.ModelForm):
        class Meta:
            model = Team
            fields = ["team_lead"]

            widgets = {
                "team_lead": AutocompleteWidget(
                    ac_class=PersonAC4,
                    attrs={
                        "required": True,
                        "disabled": True,
                    },
                    options={
                        "component_prefix": "my_prefix",
                        "placeholder": "my placeholder",
                    },
                )
            }

    create_form = FormWithSingle()

    rendered = render_template(single_form_template, {"form": create_form})

    soup = soup_from_str(rendered)

    input = soup.select_one("ul li input[type='text']")

    assert input.attrs["placeholder"] == "my placeholder"
    assert "required" in input.attrs
    assert "disabled" in input.attrs

    hx_vals = input.attrs["hx-vals"]
    assert '"placeholder": "my placeholder"' in hx_vals
    assert '"required": true' in hx_vals
    assert '"disabled": true' in hx_vals


def test_custom_options_not_required():
    class FormWithSingle(forms.ModelForm):
        class Meta:
            model = Team
            fields = ["team_lead"]

            widgets = {
                "team_lead": AutocompleteWidget(
                    ac_class=PersonAC4,
                )
            }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["team_lead"].required = False

    create_form = FormWithSingle()

    rendered = render_template(single_form_template, {"form": create_form})

    soup = soup_from_str(rendered)

    input = soup.select_one("ul li input[type='text']")

    assert "required" not in input.attrs

    hx_vals = input.attrs["hx-vals"]
    assert "required" not in hx_vals


def test_disabled_multi():

    class FormWithMulti(forms.ModelForm):
        class Meta:
            model = Team
            fields = ["members"]

            widgets = {
                "members": AutocompleteWidget(
                    ac_class=PersonAC4, options={"multiselect": True}
                )
            }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["members"].required = False
            self.fields["members"].disabled = True

    people = PersonFactory.create_batch(5)

    record = TeamFactory()
    record.members.set(people[:2])

    edit_form = FormWithMulti()
    edit_form = FormWithMulti(instance=record)

    rendered = render_template(single_form_template, {"form": edit_form})

    soup = soup_from_str(rendered)

    ac_container = soup.select_one(".ac_container")
    chips = ac_container.select("li.chip")
    assert len(chips) == 2
    for chip in chips:
        assert not chip.select_one("a")
    input_li = ac_container.select_one("li.input")
    assert not input_li.select_one("input")
    assert input_li.select_one("output#members__textinput")


def test_extra_hx_vals():
    @register
    class PersonAC4WithHxVals(PersonAC4):
        @classmethod
        def get_extra_text_input_hx_vals(cls):
            return {"extra": '"value"'}

    class FormWithSingle(forms.ModelForm):
        class Meta:
            model = Team
            fields = ["team_lead"]

            widgets = {
                "team_lead": AutocompleteWidget(
                    ac_class=PersonAC4WithHxVals,
                )
            }

    create_form = FormWithSingle()

    rendered = render_template(single_form_template, {"form": create_form})

    soup = soup_from_str(rendered)

    input = soup.select_one("ul li input[type='text']")
    hx_vals = input.attrs["hx-vals"]

    assert '"extra": "value"' in hx_vals


def test_widget_with_lazy_string_placeholder():
    from django.utils.functional import lazy

    lazy_str = lazy(lambda: "lazy placeholder", str)

    class FormWithLazyPlaceholder(forms.ModelForm):
        class Meta:
            model = Team
            fields = ["team_lead"]

            widgets = {
                "team_lead": AutocompleteWidget(
                    ac_class=PersonAC4,
                    options={"placeholder": lazy_str()},
                )
            }

    form = FormWithLazyPlaceholder()
    rendered = render_template(single_form_template, {"form": form})

    soup = soup_from_str(rendered)

    input = soup.select_one("ul li input[type='text']")

    assert input.attrs["placeholder"] == "lazy placeholder"

    hx_vals = input.attrs["hx-vals"]
    assert '"placeholder": "lazy placeholder"' in hx_vals
