"""
AppConfig configuration
"""
from django.apps import AppConfig


class AutocompleteConfig(AppConfig):
    """
    Django app config
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autocomplete'
