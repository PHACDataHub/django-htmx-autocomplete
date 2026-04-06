"""AppConfig configuration for the autocomplete app."""

from django.apps import AppConfig


class AutocompleteConfig(AppConfig):
    """Django app config for the autocomplete application."""

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "autocomplete"
