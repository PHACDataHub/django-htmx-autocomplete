"""
This file enables the component to be used like other Django widgets
"""

from django.forms import Widget

from .core import AC_CLASS_CONFIGURABLE_VALUES, Autocomplete


class AutocompleteWidget(Widget):
    template_name = "autocomplete/component.html"

    configurable_values = [
        "indicator",
        "multiselect",
        "label",
        "component_prefix",
        # the below are also configurable from the AC class
        "placeholder",
    ]

    def __init__(self, ac_class, attrs=None, options=None):
        self.ac_class = ac_class
        super().__init__(attrs)

        if not options:
            options = {}

        self.config = {}
        for k, v in options.items():
            if k in self.configurable_values:
                self.config[k] = v
            else:
                raise ValueError(f"Invalid option {k}")

    def value_from_datadict(self, data, files, name):
        if self.is_multi:
            try:
                # classic POSTs go though django's QueryDict structure
                # which has a getlist method
                value = data.getlist(name)
            except AttributeError:
                # some clients just provide lists in JSON
                value = data.get(name)

        else:
            value = data.get(name)

        return value

    def value_omitted_from_data(self, data, files, name):
        # An unselected <select multiple> doesn't appear in POST data, so it's
        # never known if the value is actually omitted.
        return []

    def get_component_id(self, field_name):
        prefix = self.get_configurable_value("component_prefix")

        return prefix + field_name

    def get_configurable_value(self, key):
        if key in self.config:
            return self.config.get(key)

        if key in AC_CLASS_CONFIGURABLE_VALUES and hasattr(self.ac_class, key):
            return getattr(self.ac_class, key)

        return None

    @property
    def is_multi(self):
        return self.get_configurable_value("multiselect")

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        proper_attrs = self.build_attrs(self.attrs, attrs)

        if value is None:
            selected_options = []
        else:
            if self.is_multi:
                selected_options = self.ac_class.get_items_from_keys(value, None)
            else:
                selected_options = self.ac_class.get_items_from_keys([value], None)

        context["ac_class"] = self.ac_class
        context["field_name"] = name
        context["id"] = attrs.get("id", self.attrs.get("id", None))
        context["route_name"] = self.ac_class.route_name

        context["disabled"] = proper_attrs.get("disabled", False)
        context["required"] = proper_attrs.get("required", False)

        context["indicator"] = self.get_configurable_value("indicator")
        context["multiselect"] = self.is_multi

        context["label"] = self.get_configurable_value("label")
        context["placeholder"] = self.get_configurable_value("placeholder")
        # context["values"] = list(self.a_c.item_values(self.a_c, selected_options))
        context["values"] = [x["key"] for x in selected_options]
        context["selected_items"] = selected_options
        context["component_prefix"] = self.get_configurable_value("component_prefix")
        context["component_id"] = self.get_component_id(name)

        return context
