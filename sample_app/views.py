from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

from autocomplete import Autocomplete, AutocompleteWidget, ModelAutocomplete, register

from .models import Person, Team


@register
class PersonAutocomplete(Autocomplete):
    @classmethod
    def search_items(cls, search, context):
        qs = Person.objects.filter(name__icontains=search)

        return [{"key": person.id, "label": person.name} for person in qs]

    @classmethod
    def get_items_from_keys(cls, keys, context):
        qs = Person.objects.filter(id__in=keys)
        return [{"key": person.id, "label": person.name} for person in qs]


class TeamForm(forms.ModelForm):
    # this form isn't meant to work for saving, we're using different "names"
    class Meta:
        model = Team
        fields = ["team_lead", "members"]
        widgets = {
            "team_lead": AutocompleteWidget(
                ac_class=PersonAutocomplete,
            ),
            "members": AutocompleteWidget(
                ac_class=PersonAutocomplete,
                options={"multiselect": True},
            ),
        }


def edit_team(request, team_id=None):
    team = Team.objects.get(id=team_id)

    form = TeamForm(instance=team, data=request.POST or None)

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(request.path)

    return render(request, "edit_team.html", {"form": form})


@register
class CustomPersonAutocomplete(PersonAutocomplete):
    no_result_text = "Keine resultate"
    narrow_search_text = "NARROW IT DOWN"
    max_results = 1
    placeholder = "Select team lead!"


@register
class CustomPersonAutocomplete2(PersonAutocomplete):
    """
    this AC is meant to be used in a form with a 'team_lead' field

    the extra-hx vals will submit an additional field when searching

    this extra param will be used by the search method
    to filter out the team_lead from the members
    """

    @classmethod
    def get_extra_text_input_hx_vals(cls):
        # single quotes not allowed here, backticks used as 2nd level quotes
        return {
            "related_team_lead": 'document.querySelector(`[name="team_lead"]`)?.value || "" ',
            # "literal": "foo", # note that this causes 'ReferenceError: foo is not defined'
            "literal": '"foo"',  # wrapping in double quotes works
        }

    @classmethod
    def search_items(cls, search, context):
        qs = Person.objects.filter(name__icontains=search)

        related_team_lead = context.client_kwargs.get("related_team_lead", None)
        if related_team_lead:
            qs = qs.exclude(id=related_team_lead)

        return [{"key": person.id, "label": person.name} for person in qs]


class TeamForm2(forms.ModelForm):
    # this form isn't meant to work for saving, we're using different "names"
    class Meta:
        model = Team
        fields = ["team_lead", "members"]
        # fields = ["team_lead"]
        widgets = {
            "team_lead": AutocompleteWidget(
                ac_class=CustomPersonAutocomplete,
                options={
                    "component_prefix": "team_lead_prefix",
                    # "placeholder": "Select team lead",
                },
                attrs={
                    "required": False,
                },
            ),
            "members": AutocompleteWidget(
                ac_class=CustomPersonAutocomplete2,
                options={"multiselect": True},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["team_lead"].required = False
        # self.fields["members"].required = False
        # self.fields["members"].disabled = True
        # self.fields["team_lead"].disabled = True


def example_with_prefix(request, team_id=None):
    team = Team.objects.get(id=team_id)

    form = TeamForm2(instance=team, data=request.POST or None)

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(request.path)

    return render(request, "edit_team.html", {"form": form})


@register
class CustomPersonAutocomplete3(ModelAutocomplete):
    model = Person
    search_attrs = ["name"]


class AnotherPersonForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["team_lead"]
        widgets = {
            "team_lead": AutocompleteWidget(
                ac_class=CustomPersonAutocomplete3,
            )
        }


def example_with_model(request, team_id=None):
    team = Team.objects.get(id=team_id)

    form = AnotherPersonForm(instance=team, data=request.POST or None)

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(request.path)

    return render(request, "edit_team.html", {"form": form})
