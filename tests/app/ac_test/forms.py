"""
Form objects used to test the autocomplete's widget interface
"""
from django import forms
from autocomplete import widgets

from .models import Person, Team
from .ac_controls import data


class SingleFormGetItem(forms.Form):
    """Form used for single select using get_items"""

    @staticmethod
    def get_items(search=None, values=None):
        """Example function used to provide list of options to widget

        Args:
            search (str, optional): Search string. Defaults to None.
            values (str[], optional): Values to return. Defaults to None.

        Returns:
            dict[]: List of dictionaries with value and label keys.
        """
        if values:
            return list(filter(lambda x: x.get("value") in values, data))

        return list(
            filter(lambda x: x.get("label").lower().startswith(search.lower()), data)
        )

    name = forms.CharField()
    company = forms.CharField(
        widget=widgets.Autocomplete(
            name="company", options=dict(get_items=get_items, minimum_search_length=0)
        )
    )


class SingleFormModel(forms.ModelForm):
    """Single select example form using a model"""

    class Meta:
        """Meta class that configures the form"""

        model = Team
        fields = ["name", "members"]
        widgets = {
            "members": widgets.Autocomplete(
                name="members", options=dict(model=Person, minimum_search_length=0)
            )
        }


class MultipleFormGetItem(forms.Form):
    """Form used for multiple select using get_items"""

    @staticmethod
    def get_items(search=None, values=None):
        """Example function used to provide list of options to widget

        Args:
            search (str, optional): Search string. Defaults to None.
            values (str[], optional): Values to return. Defaults to None.

        Returns:
            dict[]: List of dictionaries with value and label keys.
        """
        items = None
        if search is not None:
            items = Person.objects.filter(name__startswith=search)

        if values is not None:
            items = Person.objects.filter(id__in=values)

        return [{"label": x.name, "value": x.id} for x in items]

    name = forms.CharField()
    members = forms.CharField(
        widget=widgets.Autocomplete(
            name="members",
            options=dict(
                multiselect=True,
                get_items=get_items,
                route_name="multi_members",
                minimum_search_length=0,
            ),
        )
    )


class MultipleFormModel(forms.ModelForm):
    """Multiple select example form using a model"""

    class Meta:
        """Meta class that configures the form"""

        model = Team
        fields = ["name", "members"]
        widgets = {
            "members": widgets.Autocomplete(
                name="members",
                options=dict(
                    multiselect=True,
                    model=Person,
                    route_name="multi_model_members",
                    minimum_search_length=0,
                ),
            )
        }
