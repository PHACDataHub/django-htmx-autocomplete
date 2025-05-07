from django import forms
from django.forms.models import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.utils.html import mark_safe

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


class SimplestPersonFormBothFields(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["team_lead", "members"]
        widgets = {
            "team_lead": AutocompleteWidget(
                ac_class=CustomPersonAutocomplete3,
            ),
            "members": AutocompleteWidget(
                ac_class=CustomPersonAutocomplete3,
                options={"multiselect": True},
            ),
        }


def example_with_model(request, team_id=None):
    team = Team.objects.get(id=team_id)

    form = AnotherPersonForm(instance=team, data=request.POST or None)

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(request.path)

    return render(request, "edit_team.html", {"form": form})


def static_formset_example(request):
    first_3_teams_ids = {t.pk for t in Team.objects.all()[:3]}
    qs = Team.objects.filter(pk__in=first_3_teams_ids)
    formset_factory = modelformset_factory(
        Team, form=SimplestPersonFormBothFields, extra=0
    )

    if request.method == "POST":
        formset = formset_factory(request.POST, queryset=qs)
    else:
        formset = formset_factory(queryset=qs)

    if request.POST:
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(request.path)
        else:
            print(formset.errors)

    return render(request, "static_formset_example.html", {"formset": formset})


def dynamic_formset_example(request):
    # first_3_teams_ids = {t.pk for t in Team.objects.all()}
    # qs = Team.objects.filter(pk__in=first_3_teams_ids)
    qs = Team.objects.all()
    formset_factory = modelformset_factory(
        Team, form=SimplestPersonFormBothFields, extra=0
    )

    if request.method == "POST":
        formset = formset_factory(request.POST, queryset=qs, prefix="teams")
    else:
        formset = formset_factory(queryset=qs, prefix="teams")

    if request.POST:
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(request.path)
        else:
            print(formset.errors)

    return render(request, "dynamic_formset_example.html", {"formset": formset})


@register
class AutocompleteWithCustomHtmlLabels(ModelAutocomplete):
    model = Person
    search_attrs = ["name"]

    @classmethod
    def get_label_for_record(cls, record):
        # this is a custom label for the autocomplete
        # it will be used in the dropdown
        # and in the selected items
        return mark_safe(
            f"""
            <div>
                <div>{record.name}</div>
                <div style='color: red;'>{record.name.upper()}</div>
            </div>
            """
        )

    @classmethod
    def get_input_value(cls, key, label):
        return Person.objects.get(id=key).name

    @classmethod
    def get_chip_label(cls, key, label):
        name = Person.objects.get(id=key).name
        return mark_safe(
            f"""
            <span style='color: red;'>{name.upper()}</span>
            """
        )


class CustomTeamFormWithHtmlAC(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["team_lead", "members"]
        widgets = {
            "team_lead": AutocompleteWidget(
                ac_class=AutocompleteWithCustomHtmlLabels,
            ),
            "members": AutocompleteWidget(
                ac_class=AutocompleteWithCustomHtmlLabels,
                options={"multiselect": True},
            ),
        }


def example_w_html(request, team_id=None):
    team = Team.objects.get(id=team_id)

    form = CustomTeamFormWithHtmlAC(instance=team, data=request.POST or None)

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(request.path)

    return render(request, "edit_team.html", {"form": form})
