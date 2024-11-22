from dataclasses import dataclass

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

# This is the registry of registered autocomplete classes,
# i.e. the ones who respond to requests
_ac_registry = {}


AC_CLASS_CONFIGURABLE_VALUES = {
    "disabled",
    "no_result_text",
    "narrow_search_text",
    "minimum_search_length",
    "max_results",
    "component_prefix",
    "placeholder",
    "indicator",
}


def register(ac_class: type, route_name: str = None):
    if not route_name:
        route_name = ac_class.__name__

    ac_class.validate()

    if route_name in _ac_registry:
        raise ValueError(f"Autocomplete with name '{name}' is already registered.")

    ac_class.route_name = route_name

    _ac_registry[route_name] = ac_class

    return ac_class


class Autocomplete:

    no_result_text = _("No results found.")
    narrow_search_text = _(
        "Showing %(page_size)s of %(total)s items. Narrow your search for more results."
    )
    type_at_least_n_characters = _("Type at least %(n)s characters")
    minimum_search_length = 3
    max_results = 100
    component_prefix = ""

    @classmethod
    def auth_check(cls, request):
        """
        override to inspect request.user or whatever
        raise a PermissionDenied or SuspiciousOperation exception if needed
        """
        if (
            getattr(settings, "AUTOCOMPLETE_BLOCK_UNAUTHENTICATED", False)
            and not request.user.is_authenticated
        ):
            raise PermissionDenied("Must be logged in to use autocomplete")

        pass

    @classmethod
    def validate(cls):
        if not hasattr(cls, "search_items"):
            raise ValueError("You must implement a search_items method.")

        if not hasattr(cls, "get_items_from_keys"):
            raise ValueError("You must implement a get_items_from_keys method.")

    @classmethod
    def map_search_results(cls, items_iterable, selected_keys=None):
        """
        This must return a list of dictionaries with the keys "key", "label", and "selected"

        By default, we already expect search_items to return iterable of the form [{"key": "value", "label": "label"}]

        You can override this to consume paginable querysets or whatever
        """

        return [
            {  # this is the default mapping
                "key": str(i["key"]),
                "label": i["label"],
                "selected": i["key"] in selected_keys or str(i["key"]) in selected_keys,
            }
            for i in items_iterable
        ]

    @classmethod
    def get_custom_strings(cls):
        return {
            "no_results": cls.no_result_text,
            "more_results": cls.narrow_search_text,
            "type_at_least_n_characters": cls.type_at_least_n_characters,
        }

    @classmethod
    def get_extra_text_input_hx_vals(cls):
        """
        returns a dict of key/vals to go in the hx-vals attribute of the text input
        - must not contain single quotes
        - to support inline JS expressions, values are not quoted
        """

        return {}


@dataclass
class ContextArg:
    request: HttpRequest
    client_kwargs: dict
