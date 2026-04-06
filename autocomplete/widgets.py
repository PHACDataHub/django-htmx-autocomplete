"""
This file enables the component to be used like other Django widgets
"""

from typing import TYPE_CHECKING, Any, Mapping

from django.forms import Widget

from .core import AC_CLASS_CONFIGURABLE_VALUES, Autocomplete

if TYPE_CHECKING:
    from django.forms.rendering import BaseRenderer


class AutocompleteWidget(Widget):
    """Django form widget for autocomplete components.

    This widget enables using autocomplete functionality like other Django widgets.

    Attributes:
        template_name: The template used to render the widget.
        configurable_values: List of values that can be configured via options.
    """

    template_name: str = "autocomplete/component.html"

    configurable_values: list[str] = [
        "indicator",
        "multiselect",
        "label",
        "component_prefix",
        # the below are also configurable from the AC class
        "placeholder",
    ]

    def __init__(
        self,
        ac_class: type[Autocomplete],
        attrs: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the autocomplete widget.

        Args:
            ac_class: The Autocomplete class to use.
            attrs: HTML attributes for the widget.
            options: Configuration options for the widget.

        Raises:
            ValueError: If an invalid option is provided.
        """
        self.ac_class: type[Autocomplete] = ac_class
        super().__init__(attrs)

        if not options:
            options = {}

        self.config: dict[str, Any] = {}
        for k, v in options.items():
            if k in self.configurable_values:
                self.config[k] = v
            else:
                raise ValueError(f"Invalid option {k}")

    def value_from_datadict(self, data: Any, files: Any, name: str) -> Any:
        """Extract the value from the form data.

        Handles both single and multi-select modes.

        Args:
            data: The form data.
            files: Uploaded files.
            name: The field name.

        Returns:
            The extracted value(s).
        """
        if self.is_multi:
            try:
                # classic POSTs go though django's QueryDict structure
                # which has a getlist method
                value: Any = data.getlist(name)
            except AttributeError:
                # some clients just provide lists in JSON
                value = data.get(name)

        else:
            value = data.get(name)

        return value

    def value_omitted_from_data(self, data: Any, files: Any, name: str) -> bool:
        """Check if the value was omitted from the form data.

        An unselected <select multiple> doesn't appear in POST data.

        Args:
            data: The form data.
            files: Uploaded files.
            name: The field name.

        Returns:
            Always False for autocomplete widgets.
        """
        # An unselected <select multiple> doesn't appear in POST data, so it's
        # never known if the value is actually omitted.
        return False

    def get_component_id(self, field_name: str) -> str:
        """Get the component ID with prefix.

        Args:
            field_name: The field name.

        Returns:
            The prefixed component ID.
        """
        prefix: str = self.get_configurable_value("component_prefix") or ""

        return prefix + field_name

    def get_configurable_value(self, key: str) -> Any:
        """Get a configurable value from options or class defaults.

        Args:
            key: The configuration key.

        Returns:
            The configuration value or None.
        """
        if key in self.config:
            return self.config.get(key)

        if key in AC_CLASS_CONFIGURABLE_VALUES and hasattr(self.ac_class, key):
            return getattr(self.ac_class, key)

        return None

    def get_autocomplete_attr(self) -> str:
        """Get the autocomplete attribute value.

        Returns:
            The autocomplete attribute value.
        """
        value = self.get_configurable_value("autocomplete_attr")
        if value:
            return str(value)

        return "off"

    @property
    def is_multi(self) -> bool:
        """Check if this is a multi-select widget.

        Returns:
            True if multi-select is enabled.
        """
        return bool(self.get_configurable_value("multiselect"))

    def get_context(
        self, name: str, value: Any, attrs: dict[str, Any] | None
    ) -> dict[str, Any]:
        """Build the template context for rendering.

        Args:
            name: The field name.
            value: The current value.
            attrs: Additional HTML attributes.

        Returns:
            Dictionary of context variables.
        """
        context: dict[str, Any] = super().get_context(name, value, attrs)

        proper_attrs: dict[str, Any] = self.build_attrs(self.attrs, attrs)

        selected_options: list[dict[str, Any]]
        if value is None:
            selected_options = []
        else:
            if self.is_multi:
                selected_options = list(self.ac_class.get_items_from_keys(value, None))
            else:
                selected_options = list(
                    self.ac_class.get_items_from_keys([value], None)
                )

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
        context["component_prefix"] = self.get_configurable_value(
            "component_prefix"
        )
        context["component_id"] = self.get_component_id(name)

        context["autocomplete_attr_value"] = self.get_autocomplete_attr()

        return context
