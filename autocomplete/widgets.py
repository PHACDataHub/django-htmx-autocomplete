"""
This file enables the component to be used like other Django widgets
"""
from django.forms import Widget

from .autocomplete import HTMXAutoComplete


class Autocomplete(Widget):
    """
    Django forms compatible autocomplete widget

    Parameters:

        name (str):     The name of the component (must be unique)
        attrs (dict):   disabled and required attributes are supported
        options (dict): See [autocomplete.py](../autocomplete.py) for more info
            label                   (str)
            indicator               (bool) Defaults to false
            placeholder             (str)
            no_result_text          (str) Defaults to "No results found."
            narrow_search_text      (str) Defaults to
                                          "Narrow your search for more results".
            max_results             (int) Defaults to None
            minimum_search_length   (int) Defaults to 3
            multiselect             (str) Defaults to False
            model                   (str)
            item_value              (str)
            item_label              (str)
            lookup                  (str)
            get_items               (func)

    """

    template_name = "autocomplete/component.html"

    def __init__(
        self,
        name,
        options=None,
        attrs=None,
    ):
        opts = options or {}

        super().__init__(attrs)
        config = {
            "name": name,
            "disabled": attrs.get("disabled", False) if attrs else False,
            "required": attrs.get("required", False) if attrs else False,
            "indicator": opts.get("indicator", None),
            "route_name": opts.get("route_name", None),
            "label": opts.get("label", None),
            "placeholder": opts.get("placeholder", None),
            "no_result_text": opts.get("no_result_text", "No results found."),
            "narrow_search_text": opts.get(
                "narrow_search_text", "Narrow your search for more results."
            ),
            "max_results": opts.get("max_results", None),
            "minimum_search_length": opts.get("minimum_search_length", 3),
            "multiselect": opts.get("multiselect", False),
        }

        if model := opts.get("model", None):
            mdl_config = {"model": model}
            if item_value := opts.get("item_value", None):
                mdl_config["item_value"] = item_value
            if item_label := opts.get("item_label", None):
                mdl_config["item_label"] = item_label
            if lookup := opts.get("lookup", None):
                mdl_config["lookup"] = lookup

            config["Meta"] = type("Meta", (object,), mdl_config)
        else:
            config["get_items"] = opts.get("get_items", HTMXAutoComplete.get_items)

        self.a_c = type(f"HtmxAc__{name}", (HTMXAutoComplete,), config)

    def value_from_datadict(self, data, files, name):
        try:
            getter = data.getlist
        except AttributeError:
            getter = data.get
        return getter(name)

    def value_omitted_from_data(self, data, files, name):
        # An unselected <select multiple> doesn't appear in POST data, so it's
        # never known if the value is actually omitted.
        return []

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        items_selected = (
            [] if value is None else [value] if not isinstance(value, list) else value
        )
        selected_options = self.a_c.map_items(
            self.a_c,
            self.a_c.get_items(self.a_c, values=[str(x) for x in items_selected]),
        )

        context["name"] = self.a_c.name

        context["disabled"] = attrs.get("disabled", self.attrs.get("disabled", False))
        context["required"] = attrs.get("required", self.attrs.get("required", False))

        context["indicator"] = self.a_c.indicator
        context["route_name"] = self.a_c.get_route_name()
        context["label"] = self.a_c.label
        context["placeholder"] = self.a_c.placeholder
        context["multiselect"] = self.a_c.multiselect
        context["values"] = list(self.a_c.item_values(self.a_c, selected_options))
        context["selected_items"] = list(selected_options)

        self.a_c.required = context["required"]
        self.a_c.disabled = context["disabled"]

        return context
