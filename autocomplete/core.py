from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Iterable

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from django.db.models import QuerySet

# This is the registry of registered autocomplete classes,
# i.e. the ones who respond to requests
_ac_registry: dict[str, type["Autocomplete"]] = {}


AC_CLASS_CONFIGURABLE_VALUES: set[str] = {
    "disabled",
    # autocomplete_attr is the <input> attribute, used by browser to suggest values
    "autocomplete_attr",
    "no_result_text",
    "narrow_search_text",
    "minimum_search_length",
    "max_results",
    "component_prefix",
    "placeholder",
    "indicator",
}


def register(
    ac_class: type["Autocomplete"], route_name: str | None = None
) -> type["Autocomplete"]:
    """Register an Autocomplete class to make it available for use.

    Args:
        ac_class: The Autocomplete class to register.
        route_name: Optional custom route name. Defaults to class name.

    Returns:
        The registered class.

    Raises:
        ValueError: If a class with the same name is already registered.
    """
    if not route_name:
        route_name = ac_class.__name__

    ac_class.validate()

    if route_name in _ac_registry:
        raise ValueError(
            f"Autocomplete with name '{route_name}' is already registered."
        )

    ac_class.route_name = route_name

    _ac_registry[route_name] = ac_class

    return ac_class



@dataclass
class ContextArg:
    """Context passed to autocomplete methods.

    Attributes:
        request: The current HTTP request.
        client_kwargs: Dictionary of client-provided kwargs.
    """

    request: HttpRequest
    client_kwargs: dict[str, Any]


class Autocomplete:
    """Base class for implementing autocomplete functionality.

    Subclasses must implement `search_items` and `get_items_from_keys` methods.
    """

    no_result_text: str = _("No results found.")
    narrow_search_text: str = _(
        "Showing %(page_size)s of %(total)s items. Narrow your search for more results."
    )
    type_at_least_n_characters: str = _("Type at least %(n)s characters")
    minimum_search_length: int = 3
    max_results: int = 100
    component_prefix: str = ""
    route_name: str = ""  # Set by register()

    @classmethod
    def auth_check(cls, request: HttpRequest) -> None:
        """Override to inspect request.user or raise PermissionDenied if needed.

        Args:
            request: The current HTTP request.

        Raises:
            PermissionDenied: If user authentication check fails.
        """
        if (
            getattr(settings, "AUTOCOMPLETE_BLOCK_UNAUTHENTICATED", False)
            and not request.user.is_authenticated
        ):
            raise PermissionDenied("Must be logged in to use autocomplete")

    @classmethod
    def validate(cls) -> None:
        """Validate that required methods are implemented.

        Raises:
            ValueError: If required methods are missing.
        """
        if not hasattr(cls, "search_items"):
            raise ValueError("You must implement a search_items method.")

        if not hasattr(cls, "get_items_from_keys"):
            raise ValueError("You must implement a get_items_from_keys method.")

    @classmethod
    def map_search_results(
        cls,
        items_iterable: Iterable[dict[str, Any]],
        selected_keys: Iterable[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Map search results to a standardized format.

        This must return a list of dictionaries with the keys "key", "label", and "selected".

        By default, we already expect search_items to return iterable of the
        form [{"key": "value", "label": "label"}]

        You can override this to consume paginable querysets or whatever.

        Args:
            items_iterable: Iterable of item dictionaries.
            selected_keys: Keys of currently selected items.

        Returns:
            List of mapped item dictionaries with key, label, and selected status.
        """
        if selected_keys is None:
            selected_keys = []

        return [
            {  # this is the default mapping
                "key": str(i["key"]),
                "label": i["label"],
                "selected": i["key"] in selected_keys or str(i["key"]) in selected_keys,
            }
            for i in items_iterable
        ]

    @classmethod
    def get_custom_strings(cls) -> dict[str, str]:
        """Get custom display strings for the autocomplete component.

        Returns:
            Dictionary of custom string keys to their values.
        """
        return {
            "no_results": cls.no_result_text,
            "more_results": cls.narrow_search_text,
            "type_at_least_n_characters": cls.type_at_least_n_characters,
        }

    @classmethod
    def get_extra_text_input_hx_vals(cls) -> dict[str, str]:
        """Get extra HTMX hx-vals for the text input.

        Returns a dict of key/vals to go in the hx-vals attribute of the text input.
        - must not contain single quotes
        - to support inline JS expressions, values are not quoted

        Returns:
            Dictionary of extra hx-vals.
        """
        return {}

    @classmethod
    def get_input_value(cls, key: str, label: str) -> str:
        """Get the display value for the text input in single-select mode.

        This is the value that will be shown in the text input.
        Override is useful if labels have HTML, or need shortening.

        Args:
            key: The item key.
            label: The item label.

        Returns:
            The display value for the input.
        """
        return label

    @classmethod
    def get_chip_label(cls, key: str, label: str) -> str:
        """Get the display label for chips in multi-select mode.

        This is the value that will be shown in the chip.
        Override is useful if options are big and need shortening.

        Args:
            key: The item key.
            label: The item label.

        Returns:
            The chip display label.
        """
        return label

    @classmethod
    def search_items(cls, search: str, context: ContextArg) -> Iterable[dict[str, Any]]:
        """Search for items matching the query.

        Must be implemented by subclasses.

        Args:
            search: The search query string.
            context: Context containing request and client kwargs.

        Returns:
            Iterable of item dictionaries with "key" and "label".
        """
        raise NotImplementedError("Subclasses must implement search_items")

    @classmethod
    def get_items_from_keys(
        cls, keys: Iterable[str], context: ContextArg | None
    ) -> Iterable[dict[str, Any]]:
        """Get items by their keys.

        Must be implemented by subclasses.

        Args:
            keys: Iterable of item keys.
            context: Context containing request and client kwargs, or None.

        Returns:
            Iterable of item dictionaries with "key" and "label".
        """
        raise NotImplementedError("Subclasses must implement get_items_from_keys")


