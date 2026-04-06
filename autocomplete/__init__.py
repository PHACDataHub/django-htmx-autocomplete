"""
Allow HTMXAutoComplete to be imported from the module directly
"""

from .core import Autocomplete, register
from .shortcuts import ModelAutocomplete
from .views import urls
from .widgets import AutocompleteWidget

__all__ = [
    "Autocomplete",
    "ModelAutocomplete",
    "register",
    "urls",
    "AutocompleteWidget",
]
