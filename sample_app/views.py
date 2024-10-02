from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

from autocomplete import Autocomplete, AutocompleteWidget, register

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
