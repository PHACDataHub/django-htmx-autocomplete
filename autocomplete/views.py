from typing import TYPE_CHECKING, Any

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import path
from django.utils.functional import cached_property
from django.views import View

from .core import (
    AC_CLASS_CONFIGURABLE_VALUES,
    Autocomplete,
    ContextArg,
    _ac_registry,
)

if TYPE_CHECKING:
    from collections.abc import Iterable
    from django.db.models import QuerySet


class AutocompleteBaseView(View):
    """Base view for autocomplete HTTP endpoints."""

    kwargs: dict[str, Any]

    @cached_property
    def ac_class(self) -> type[Autocomplete]:
        """Get the registered autocomplete class for this request.

        Returns:
            The registered Autocomplete class.

        Raises:
            ValueError: If no autocomplete is registered with the given name.
        """
        ac_name: str = self.kwargs["ac_name"]

        try:
            return _ac_registry[ac_name]

        except KeyError as e:
            raise ValueError(
                f"No registered autocomplete with name {ac_name}"
            ) from e

    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """Dispatch the request after checking authentication."""
        self.ac_class.auth_check(request)

        return super().dispatch(request, *args, **kwargs)

    @cached_property
    def request_dict(self) -> dict[str, str]:
        """Convert the request's QueryDict into a regular dict.

        Returns:
            Dictionary of GET parameters.
        """
        return self.request.GET.dict()

    def get_field_name(self) -> str:
        """Get the field name from the request.

        Returns:
            The field name parameter.
        """
        return self.request_dict["field_name"]

    def get_component_id(self) -> str:
        """Get the component ID with prefix.

        Returns:
            The prefixed component ID.
        """
        prefix: str = self.get_configurable_value("component_prefix") or ""

        return prefix + self.get_field_name()

    def get_configurable_value(self, key: str) -> Any:
        """Get a configurable value from request or class defaults.

        Args:
            key: The configuration key to look up.

        Returns:
            The configuration value or None.
        """
        if key in self.request_dict:
            return self.request.GET.get(key)

        if key in AC_CLASS_CONFIGURABLE_VALUES and hasattr(self.ac_class, key):
            return getattr(self.ac_class, key)

        return None

    def get_autocomplete_attr(self) -> str:
        """Return the value for the autocomplete attribute.

        Returns:
            The autocomplete attribute value.
        """
        autocomplete_value = self.get_configurable_value("autocomplete_attr")

        if autocomplete_value is not None:
            return str(autocomplete_value)

        return "off"

    def get_template_context(self) -> dict[str, Any]:
        """Build the template context for rendering.

        Returns:
            Dictionary of context variables for templates.
        """
        return {
            "route_name": self.ac_class.route_name,
            "ac_class": self.ac_class,
            "field_name": self.get_field_name(),
            "component_id": self.get_component_id(),
            "required": bool(self.get_configurable_value("required")),
            "placeholder": self.get_configurable_value("placeholder"),
            "indicator": self.get_configurable_value("indicator"),
            "custom_strings": self.ac_class.get_custom_strings(),
            "multiselect": bool(self.get_configurable_value("multiselect")),
            "component_prefix": self.get_configurable_value(
                "component_prefix"
            ),
            "disabled": bool(self.get_configurable_value("disabled")),
            "autocomplete_attr_value": self.get_autocomplete_attr(),
        }


def toggle_set(_set: set[str], item: str) -> set[str]:
    """Toggle an item in a set.

    Removes the item if present, adds it if not.
    Handles string/int key comparison.

    Args:
        _set: The set to toggle within.
        item: The item to toggle.

    Returns:
        A new set with the item toggled.
    """
    s: set[str] = _set.copy()

    if item in s:
        s.remove(item)

    elif str(item) in s:
        s.remove(str(item))

    elif item in {str(x) for x in s}:
        s = {x for x in s if str(x) != item}

    else:
        s.add(item)

    return s


def replace_or_toggle(_set: set[str], item: str) -> set[str]:
    """Toggle or replace items in a set for single-select mode.

    In the case of 'toggling' one item, we remove it if the item is
    already selected, otherwise we replace the item with the new different one.

    Args:
        _set: The set (must contain at most one item).
        item: The item to toggle or replace with.

    Returns:
        The updated set.

    Raises:
        Exception: If the set has more than one item.
    """
    if len(_set) > 1:
        raise Exception("this function is only for sets with one item")

    toggled = toggle_set(_set, item)

    if len(toggled) > 1:
        return {item}

    return toggled


class ToggleView(AutocompleteBaseView):
    """View to toggle selection of an autocomplete item."""

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """Handle GET request to toggle an item selection."""
        field_name: str = self.request_dict["field_name"]

        current_items: list[str] = self.request.GET.getlist(field_name)
        if current_items == ["undefined"] or current_items == [""]:
            current_items = []

        key_to_toggle: str | None = request.GET.get("item")

        if key_to_toggle is None:
            return HttpResponseBadRequest()

        is_multi: bool = bool(self.get_configurable_value("multiselect"))

        if is_multi:
            new_selected_keys: set[str] = toggle_set(
                set(current_items), key_to_toggle
            )
        else:
            new_selected_keys = replace_or_toggle(
                set(current_items), key_to_toggle
            )
        keys_to_fetch: set[str] = set(new_selected_keys).union({key_to_toggle})

        context_obj = ContextArg(request=request, client_kwargs=request.GET)
        all_values = self.ac_class.get_items_from_keys(
            keys_to_fetch, context_obj
        )

        items = self.ac_class.map_search_results(all_values, new_selected_keys)

        # OOB is used if the user clicks the X on a chip,
        # to update the selected style of the option
        # if it is currently in the dropdown list
        swap_oob: bool = bool(request.GET.get("remove", False))

        target_item: dict[str, Any] | None = next(
            (x for x in items if x["key"] == key_to_toggle), None
        )

        new_items: list[dict[str, Any]] = [
            x for x in items if x["key"] in new_selected_keys
        ]

        def sort_items(item: dict[str, Any]) -> int:
            try:
                return current_items.index(f"{item['key']}")
            except ValueError:
                return len(new_items)

        new_items = sorted(new_items, key=sort_items)

        if target_item is None:
            raise ValueError("Requested item to toggle not found.")

        return render(
            request,
            "autocomplete/item.html",
            {
                **self.get_template_context(),
                "search": "",
                "values": new_selected_keys,
                "item_as_list": [target_item],
                "item": target_item,
                "toggle": new_items,
                "swap_oob": swap_oob,
            },
        )


class ItemsView(AutocompleteBaseView):
    """View to search and list autocomplete items."""

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """Handle GET request to search for items."""
        context_obj = ContextArg(request=request, client_kwargs=request.GET)

        search_query: str = request.GET.get("search", "")
        field_name: str | None = self.get_configurable_value("field_name")
        selected_keys: list[str] = request.GET.getlist(field_name or "")
        if selected_keys == [""]:
            selected_keys = []

        if selected_keys:
            selected_items = self.ac_class.get_items_from_keys(
                selected_keys, context_obj
            )
        else:
            selected_items = []

        query_too_short: bool = (
            len(search_query) < self.ac_class.minimum_search_length
        )

        if query_too_short:
            search_results: Iterable[dict[str, Any]] = []
        else:
            search_results = self.ac_class.search_items(
                search_query,
                context_obj,
            )

        all_items: list[dict[str, Any]] = [*selected_items]
        for i in search_results:
            if str(i["key"]) not in selected_keys:
                all_items.append(i)

        total_results: int = len(all_items)
        cutoff: int = self.ac_class.max_results + len(selected_keys)
        if total_results > cutoff:
            all_items = all_items[:cutoff]

        mapped_items = self.ac_class.map_search_results(
            all_items, selected_keys
        )

        # render items ...
        return render(
            request,
            "autocomplete/item_list.html",
            {
                # note: name -> field_name
                **self.get_template_context(),
                "show": not (query_too_short),
                "query_too_short": query_too_short,
                "search": search_query,
                "items": mapped_items,
                "total_results": total_results,
                "minimum_search_length": self.ac_class.minimum_search_length,
            },
        )


urls = (
    [
        path(
            "autocomplete/<str:ac_name>/items",
            ItemsView.as_view(),
            name="items",
        ),
        path(
            "autocomplete/<str:ac_name>/toggle",
            ToggleView.as_view(),
            name="toggle",
        ),
    ],
    "autocomplete",
    "autocomplete",
)
