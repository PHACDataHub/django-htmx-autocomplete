"""
Django HTMX Autocomplete

This file contains the main functionality of the component.
"""
import re

from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    QueryDict,
    HttpResponseNotFound,
)
from django.views import View
from django.template import loader
from django.urls import re_path
from django.core.exceptions import ImproperlyConfigured
from django.apps import apps
from django.db import models
from django.db.models.fields import CharField

# The acceptable regex of the name attribute
NAME_PATTERN = r"^[a-zA-Z_$][0-9a-zA-Z_$]*$"


class HTMXAutoComplete(View):
    """Abstract base class for autocomplete component instances

    Create new autocomplete components by extending this class and configuring
    the required parameters.  Many of the parameters are verified by the
    `verify_config` class method and will throw errors if not properly
    configured.  This mechanism is meant only to assist developers and should
    not be relied upon.

    Required attributes:

        name (str): The name attribute determines the name of the underlying
                    form element and should be unique in your application.  It
                    will be  used as the name of the url pattern and by default
                    is appended to the URL of the component's views.  The
                    uniqueness of the name is not verified, but it must match
                    the regex pattern `NAME_PATTERN`.

        In simple cases we can link the component to a Django model by adding a
        Meta subclass that defined the model related metadata.

        class Meta:

            model:       A valid Django model or string ('app.model')

        Optionally the following attributes can also be defined:

            item_value:  The column string or DeferredAttribute that will be
                         used as the item value.  (Defaults to the PK)

            item_label: The column string or DeferredAttribute that will be
                         used as the item's label and used for searches.
                         Defaults to the first CharField, or the first field if
                         no CharFields exist.

        For more fine-grained control over what items are available, you can
        also override the `get_items` function.

        Note: You must either add a `Meta.model` attribute or override
        `get_items`.  If you do both the defined model is accessible via
        `self.Meta.model`, and the `item_value` and `item_label` properties are
        accessible as `self._item_value` and `self._item_label` respectively.

    Optional attributes:

    label (str or None):          The label to use for the component (in HTML)
                                  If defined it must be a string.
                                  Defaults to None.

    placeholder (str or None):    The placeholder text used on the component
                                  Defaults to None.

    no_result_text (str):         The string displayed when no results are found.
                                  Defaults to "No results found."

    max_results (int):            The maximum number of search results to return to the
                                  frontend, or None for all.
                                  Defaults to None.

    narrow_search_text (str):     Text to display when the results are cut off due to
                                  max_results.
                                  Default: "Narrow your search for more results."

    minimum_search_length (int):  The minimum search length to perform a search
                                  and show the dropdown.
                                  Defaults to 3.

    multiselect (boolean):        Determines if a user can select multiple items
                                  from the dropdown, or only 1.
                                  Defaults to False.

    """

    # Used for routing and input names.  (abstract, must be unique)
    name = None

    # If specified use this string instead of name for the route name
    route_name = None

    # The component label passed to the template.
    label = None

    # The placeholder text.  (Typically something like "Type to search...")
    placeholder = None

    # The minimum search length to perform a search and show the dropdown.
    minimum_search_length = 3

    # The maximum number of search results to return to the frontend, or None for all
    max_results = None

    # Text to display when the results are cut off due to max_results.
    narrow_search_text = "Narrow your search for more results"

    # The text displayed when no results are found.
    no_result_text = "No results found."

    # If True will allow the user to select multiple items
    multiselect = False

    # Used internally to reference the `value` field returned by `get_items`
    _item_value = "value"

    # Used internally to reference the `label` field returned by `get_items`
    _item_label = "label"

    @classmethod
    def url_dispatcher(cls, route):
        """Return the url pattern required for the component to function.

        Note: Calling this method on the base class returns an array of all
        subclassed url dispatchers.

        Calling this method also verifies the configuration of the component.

        The following routes will be included in the pattern:
        GET /{route}/{route_name}/items
        GET /{route}/{route_name}/component
        PUT /{route}/{route_name}/toggle

        Parameters:
        route (str): The base URL to use when creating the route.

        Returns:
        django.urls.URLPattern
        """
        if cls == HTMXAutoComplete:
            return [cls.url_dispatcher(route) for cls in cls.__subclasses__()]

        cls.verify_config()
        prefix = f"{route}/{cls.get_route_name()}"
        return re_path(
            f"{prefix}/(?P<method>items|component|toggle)$",
            cls.as_view(),
            name=cls.get_route_name(),
        )

    @classmethod
    def _verify_label(cls):
        """Test label validity"""
        if (
            hasattr(cls, "label")
            and cls.label is not None
            and not isinstance(cls.label, str)
        ):
            raise ImproperlyConfigured("`label` must be a string.")

    @classmethod
    def _verify_name(cls):
        """Test that name is present and valid"""
        if not isinstance(cls.name, str):
            raise ImproperlyConfigured(
                "`name` must a string and defined on the subclass."
            )

        if not re.match(NAME_PATTERN, cls.name):
            raise ImproperlyConfigured(
                f"`name` must match the following regex pattern: {NAME_PATTERN}"
            )

    @classmethod
    def _verify_route_name(cls):
        """Test that route_name is valid and unique"""

        if cls.route_name is not None and not re.match(NAME_PATTERN, cls.route_name):
            raise ImproperlyConfigured(
                f"`route_name` must match regex pattern: {NAME_PATTERN}"
            )

        if cls.get_route_name() in [
            cl.get_route_name() if cl is not cls else ""
            for cl in HTMXAutoComplete.__subclasses__()
        ]:
            raise ImproperlyConfigured(
                "Autocomplete components must have a unique route_name.  The "
                f"name {cls.get_route_name()}` is already in defined."
            )

    @classmethod
    def _verify_model_or_get_items(cls):
        """Test for meta options or get_items"""
        if not hasattr(cls, "Meta") and HTMXAutoComplete.get_items == cls.get_items:
            raise ImproperlyConfigured(
                "You must either define a `Meta` class or override `get_items`"
            )

    @classmethod
    def _get_and_verify_model(cls, meta):
        """Test that model is defined and valid
        Returns model object"""

        if not hasattr(meta, "model") or meta.model is None:
            raise ImproperlyConfigured("You must set `model` in the `Meta` class.")
        if isinstance(meta.model, str):
            if not "." in meta.model:
                raise ImproperlyConfigured(
                    "Meta.model should be an object or string in the format"
                    " app.model"
                )
            try:
                return apps.get_model(meta.model)
            except Exception as exp:
                raise ImproperlyConfigured(f"Error loading '{meta.model}'") from exp
        elif not isinstance(meta.model, models.base.ModelBase):
            raise ImproperlyConfigured(
                "Meta.model should be an object or string in the format \"app.model\""
            )
        return meta.model

    @classmethod
    def _get_and_verify_item_value(cls, meta):
        """Verify and get item_value"""
        if hasattr(meta, "item_value"):
            if not isinstance(meta.item_value, str) and not isinstance(
                meta.item_value, models.query_utils.DeferredAttribute
            ):
                raise ImproperlyConfigured(
                    "If Meta.item_value is defined it must be a valid "
                    "column attribute"
                )
            if not isinstance(meta.item_value, str):
                return meta.item_value.field.name

            return meta.item_value

        return meta.model._meta.pk.name  # pylint: disable=protected-access

    @classmethod
    def _get_and_verify_item_label(cls, meta):
        if hasattr(meta, "item_label"):
            if not isinstance(meta.item_label, str) and not isinstance(
                meta.item_label, models.query_utils.DeferredAttribute
            ):
                raise ImproperlyConfigured(
                    "If Meta.item_label is defined it must be a valid "
                    "column attribute"
                )
            if not isinstance(meta.item_label, str):
                return meta.item_label.field.name
            return meta.item_label

        all_fields = meta.model._meta.fields  # pylint: disable=protected-access
        if len(all_fields) == 0:
            raise ImproperlyConfigured("The chosen model has no fields.")

        char_fields = list(filter(lambda x: isinstance(x, CharField), all_fields))
        if len(char_fields) > 0:
            return char_fields[0].name

        return all_fields[0].name

    @classmethod
    def verify_config(cls):
        """Verify that the component is correctly configured.

        Raises django.core.exceptions.ImproperlyConfigured
        """

        cls._verify_label()
        cls._verify_name()
        cls._verify_route_name()
        cls._verify_model_or_get_items()

        if hasattr(cls, "Meta"):
            cls.Meta.model = cls._get_and_verify_model(cls.Meta)
            cls._item_value = cls._get_and_verify_item_value(cls.Meta)
            cls._item_label = cls._get_and_verify_item_label(cls.Meta)

    @classmethod
    def get_route_name(cls):
        """Return the name to use for routes

        Returns:
            str: Name to use for routes
        """
        return cls.route_name if cls.route_name else cls.name

    def get_items(self, search=None, values=None):
        """Get available items based on search or values.

        If search is specified, only items who's label contain the search
        term will be included in the results.  The label column is defined by
        the Meta class's `item_label` attribute.

        If values is specified, only items who's value is contained in the
        values array will be included in the results.  The value column is
        defined by the Meta class's `item_value` attribute.

        This method can be overridden to provide more advanced control over
        how items are searched for or generated.  In the case where the Meta
        class is not specified at all, the overridden method is expected to
        return an array of dictionaries where each item has the `label` and
        value` keys defined.

        Parameters:
        search (str): The search term
        values (str[]): Array of values

        Returns:
        array of dictionaries
        """
        items = None
        if search is not None:
            search_dict = {self._item_label + "__icontains": search}
            # pylint: disable=no-member
            items = self.Meta.model.objects.filter(**search_dict)

        if values is not None:
            search_dict = {self._item_value + "__in": values}
            # pylint: disable=no-member
            items = self.Meta.model.objects.filter(**search_dict)

        return items.values() if items is not None else []

    def map_items(self, items, selected=None):
        """Return an array of dictionaries suitable for use by the templates."""
        return list(
            map(
                lambda o: {
                    "label": str(o.get(self._item_label)),
                    "value": str(o.get(self._item_value)),
                    "selected": str(o.get(self._item_value)) in selected
                    if selected
                    else False,
                },
                items,
            )
        )

    def item_values(self, items, only_selected=False):
        """Returns a list of values.

        Typically used to set the form element's value.

        only_selected(bool):  If set to True only the items with selected=True
                              will be used.
        """
        return map(
            lambda x: str(x.get("value")),
            filter(lambda x: not only_selected or x.get("selected"), items),
        )

    def put(self, request, method):
        """Handler for PUT /{route}/{name}/toggle

        A toggle request should include the item being toggled as well as the
        currently selected items.  This is because the response template will
        include an updated list of selected items - and the state of what items
        are selected is stored in the browser.  The currently selected items are
        also used to determine if the item is selected or not.

        Payload:
            {name} (list): List of values currently "selected".
            item (str): The value of the item being toggled.

        Returns:
            HTMX responsible to update selected items displayed in the browser.
            (autocomplete/item.html)

            Context:
                name (str): Name of this component (for html elements)
                route_name (str): Name to use to get routes
                multiselect (bool): Can the user select multiple items?
                values (list): Updated list of values
                item (dict): The item object being toggled
                selected_items (dict[]): Updated list of selected items
                swap_oob (bool): If True the returned item will be swapped out
                    of band.  (Used if the user clicks the X on a chip, to
                    update the selected style of the option if it is currently
                    in the dropdown list)

        """
        data = QueryDict(request.body)
        items_selected = data.getlist(self.name)

        if method == "toggle":
            item = data.get("item", None)
            if item is None:
                return HttpResponseBadRequest()

            items = self.map_items(
                self.get_items(values=items_selected + [item]), items_selected
            )

            target_item = next((x for x in items if x.get("value") == item), None)

            if target_item is None:
                print("ERROR: Requested item to toggle not found.")
                return HttpResponseNotFound()

            if not self.multiselect:
                for item in items:
                    item["selected"] = False

            if target_item.get("selected"):
                items.remove(target_item)
                target_item["selected"] = False
            else:
                target_item["selected"] = True

            template = loader.get_template("autocomplete/item.html")
            return HttpResponse(
                template.render(
                    {
                        "name": self.name,
                        "no_result_text": self.no_result_text,
                        "narrow_search_text": self.narrow_search_text,
                        "route_name": self.get_route_name(),
                        "multiselect": self.multiselect,
                        "values": self.item_values(items, True),
                        "item": target_item,
                        "toggle": items,
                        "swap_oob": data.get("remove", False),
                    }
                ),
                request,
            )

        return HttpResponseBadRequest()

    def get(self, request, method):
        """Handler for GET /{route}/{name}/component and /{route}/{name}/items

        Common query parameters:
            {name} (list): List of values currently "selected".

        GET /{route}/{name}/component
            Renders the component itself.

            Returns:
                HTMX responsible to render the root of the component.
                (autocomplete/component.html)

                This can be used for initial rendering or to perform live
                updates after events such as on `blur`.
                Notice: The default implementation does not re-render on blur.

                Context:
                    name (str): Name of this component
                    route_name (str): Name to use to get routes
                    label (str): The label of the control (or None)
                    placeholder (str): The placeholder text (or None)
                    multiselect (bool): Can the user selected multiple items?
                    values (list): List of selected values
                    selected_items (dict[]): List of selected items

        GET /{route}/{name}/items
            Renders the list of items for the dropdown.

            Additional query parameters:
            search (str): Search string used to filter the returned items

            Returns:
                HTMX responsible to render the list of available items.

                Context:
                    name (str): Name of this component
                    route_name (str): Name to use to get routes
                    search (str): The search string (if any)
                    show (bool): Whether or not the dropdown should be shown
                    items (dict[]): List of items
        """
        items_selected = request.GET.getlist(self.name)

        if method == "component":
            template = loader.get_template(
                "autocomplete/component.html"
            )
            selected_options = self.map_items(self.get_items(values=items_selected))

            return HttpResponse(
                template.render(
                    {
                        "name": self.name,
                        "route_name": self.get_route_name(),
                        "label": self.label,
                        "placeholder": self.placeholder,
                        "multiselect": self.multiselect,
                        "values": self.item_values(selected_options),
                        "selected_items": selected_options,
                        "no_result_text": self.no_result_text,
                        "narrow_search_text": self.narrow_search_text,
                    },
                    request,
                )
            )

        if method == "items":
            template = loader.get_template(
                "autocomplete/item_list.html"
            )
            search = request.GET.get("search", "")
            show = len(search) >= self.minimum_search_length
            items = (
                self.map_items(self.get_items(search), items_selected) if show else []
            )
            total_results = len(items)
            if self.max_results is not None and len(items) > self.max_results:
                items = items[:self.max_results]

            return HttpResponse(
                template.render(
                    {
                        "name": self.name,
                        "no_result_text": self.no_result_text,
                        "narrow_search_text": self.narrow_search_text,
                        "route_name": self.get_route_name(),
                        "show": show,
                        "items": items,
                        "total_results": total_results,
                    },
                    request,
                )
            )

        return HttpResponseBadRequest()
