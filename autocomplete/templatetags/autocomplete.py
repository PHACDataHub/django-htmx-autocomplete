"""
Django template tags to facilitate rendering of the component
"""

import hashlib
import json
from typing import TYPE_CHECKING, Any

from django import template, urls
from django.template import loader, Context
from django.template.defaultfilters import stringfilter
from django.utils.html import escape, format_html
from django.utils.http import urlencode
from django.utils.safestring import SafeString, mark_safe

if TYPE_CHECKING:
    from collections.abc import Mapping

register: template.Library = template.Library()


@register.filter
@stringfilter
def make_id(value: str) -> str:
    """Generate an ID given a string, to use as element IDs in HTML.

    Args:
        value: The string to hash.

    Returns:
        SHA1 hash of the value.
    """
    return hashlib.sha1(value.encode("utf-8")).hexdigest()


@register.filter()
@stringfilter
def search_highlight(value: str, search: str) -> str:
    """Surround the section of text matching the search with a classed span.

    Args:
        value: The text to highlight.
        search: The search query to highlight.

    Returns:
        HTML string with highlighted search term.
    """
    # if the value has HTML, don't bother to highlight anything
    if isinstance(value, SafeString) and escape(value) != value:
        return value

    if search == "":
        return value
    try:
        pos: int = value.lower().index(search.lower())
        start: str = escape(value[:pos])
        match: str = escape(value[pos : pos + len(search)])
        end: str = escape(value[pos + len(search) :])
        return mark_safe(f'{start}<span class="highlight">{match}</span>{end}')
    except ValueError:
        pass
    return value


@register.simple_tag(takes_context=True)
def use_string(context: Context, name: str, strings: dict[str, str]) -> str:
    """
    Loads the string from a template or via the variable dict `strings` if the `name`
    key is defined within. This allows strings to be overridden in 2 ways, either by
    user defined templates which will override *all* instances, or via the
    `custom_strings` property of the Autocomplete instance which allows individual
    customization.

    When `name` is not found in `strings`, the template name becomes:

    autocomplete/strings/{name}.html

    Args:
        context: The template context.
        name: The string key to look up.
        strings: Dictionary of custom strings.

    Returns:
        The resolved string value.
    """
    if name in strings:
        return strings[name]

    return loader.get_template(
        f"autocomplete/strings/{name}.html", using="django"
    ).render(context.flatten())


@register.simple_tag
def substitute_string(template_str: str, **kwargs: Any) -> str:
    """
    Substitute the template string with the kwargs.

    Args:
        template_str: The template string with placeholders.
        **kwargs: Values to substitute.

    Returns:
        The formatted string.
    """
    as_strings: dict[str, str] = {k: str(v) for k, v in kwargs.items()}
    return template_str % as_strings


@register.simple_tag
def autocomplete(name: str, selected: list[Any] | None = None) -> str:
    """
    Tag used to render autocomplete component in a Django Template.

    Parameters:
        name: Name of the component.
              The name is used to generate routes and must be unique.
              Required.
        selected: List of selected values.
                  Defaults to None.

    Returns:
        HTML div element with HTMX attributes to load the component.
    """
    options_selected: str = (
        ",".join([str(x) for x in selected]) if selected is not None else ""
    )

    url: str = urls.reverse(name, kwargs={"method": "component"})
    parameter: str = urlencode({name: options_selected})
    get_url: str = f"{url}?{parameter}"

    return format_html(
        (f'<div hx-get="{get_url}"hx-trigger="load"hx-swap="outerHTML"></div>')
    )


@register.filter
def js_boolean(value: Any) -> str:
    """
    Convert the value to a javascript boolean.

    Args:
        value: The value to convert.

    Returns:
        "true" if truthy, "false" otherwise.
    """
    return "true" if value else "false"


@register.simple_tag
def autocomplete_head(bootstrap: bool = False) -> str:
    """
    Renders the styles required for the component.

    Parameters:
        bootstrap: Set to true if the bootstrap css should be loaded from cdn.
                   Defaults to False.

    Returns:
        Rendered HTML for head styles.
    """
    return loader.get_template(
        "autocomplete/head.html", using="django"
    ).render({"bootstrap": bootstrap})


@register.simple_tag(takes_context=True)
def autocomplete_scripts(
    context: Context,
    bootstrap: bool = False,
    htmx: bool = False,
    htmx_csrf: bool = False,
) -> str:
    """
    Renders the required script tags for the component.

    Args:
        bootstrap: Set to true if bootstrap should be loaded from cdn.
                   Defaults to False.
        htmx: Set to true if htmx should be loaded from cdn.
              Defaults to False.
        htmx_csrf: Set to true if htmx should be initialized with csrf token.
                   Defaults to False.

    Returns:
        Rendered HTML for script tags.
    """
    return loader.get_template("autocomplete/scripts.html", using="django").render(
        {
            "csrf_token": context.get("csrf_token", ""),
            "bootstrap": bootstrap,
            "htmx": htmx,
            "htmx_csrf": htmx_csrf,
        }
    )


@register.simple_tag
def value_if_truthy(test: Any, value: str, default: str = "") -> str:
    """
    Return the value if it is truthy, otherwise return the default.

    Args:
        test: The value to test.
        value: The value to return if test is truthy.
        default: The default value if test is falsy.

    Returns:
        value if test is truthy, default otherwise.
    """
    return value if test else default


@register.simple_tag(takes_context=True)
def base_configurable_values_hx_params(context: Context) -> str:
    """Build the hx-params attribute value for base configurable values.

    Args:
        context: The template context.

    Returns:
        Comma-separated string of parameter names.
    """
    field_name: Any = context.get("field_name")
    required: Any = context.get("required")
    disabled: Any = context.get("disabled")
    placeholder: Any = context.get("placeholder")
    multiselect: Any = context.get("multiselect")

    hx_params: str = f"{field_name},field_name,item,component_prefix"

    if required:
        hx_params += ",required"

    if disabled:
        hx_params += ",disabled"

    if placeholder:
        hx_params += ",placeholder"

    if multiselect:
        hx_params += ",multiselect"

    return mark_safe(hx_params)


@register.simple_tag(takes_context=True)
def base_configurable_hx_vals(context: Context) -> str:
    """
    json-like format
    must be wrapped in curly braces

    Args:
        context: The template context.

    Returns:
        JSON-like string for hx-vals attribute (without braces).
    """
    field_name: Any = context.get("field_name")
    required: Any = context.get("required")
    disabled: Any = context.get("disabled")
    placeholder: Any = context.get("placeholder")
    multiselect: Any = context.get("multiselect")
    component_prefix: Any = context.get("component_prefix")

    props: dict[str, Any] = {
        "field_name": escape(field_name),
        "component_prefix": escape(component_prefix),
    }

    if required:
        props["required"] = bool(required)

    if disabled:
        props["disabled"] = bool(disabled)

    if multiselect:
        props["multiselect"] = bool(multiselect)

    if placeholder:
        props["placeholder"] = escape(str(placeholder))

    hx_vals: str = json.dumps(props).replace("{", "").replace("}", "")

    return mark_safe(hx_vals)


def stringify_extra_hx_vals(extra_hx_vals_dict: dict[str, str]) -> str:
    """Convert extra hx-vals dict to string format.

    Args:
        extra_hx_vals_dict: Dictionary of extra hx-vals.

    Returns:
        Comma-separated string of key: value pairs.

    Raises:
        ValueError: If any value contains single quotes.
    """
    if any("'" in val for val in extra_hx_vals_dict.values()):
        raise ValueError(
            "Extra hx vals cannot contain single quotes, consider backticks for JS expressions or escaping double-quotes"
        )

    return ",".join([f' "{key}": {val}' for key, val in extra_hx_vals_dict.items()])


@register.simple_tag(takes_context=True)
def text_input_hx_vals(context: Context) -> str:
    """
    items has augments hx-vals,
    - it adds JS value of the search input
    - users can add more values in their class

    Args:
        context: The template context.

    Returns:
        JavaScript expression string for hx-vals.
    """
    base_hx_vals_str: str = base_configurable_hx_vals(context)

    component_id_escape: str = escape(context.get("component_id", ""))

    val: str = (
        "js:{"
        f"{base_hx_vals_str},"
        f'search: document.getElementById("{component_id_escape}__textinput").value'
    )

    ac_class: Any = context.get("ac_class")
    extra_hx_vals: dict[str, str] = {}
    if ac_class is not None:
        extra_hx_vals = ac_class.get_extra_text_input_hx_vals()
    if extra_hx_vals:
        extra_hx_val_str: str = stringify_extra_hx_vals(extra_hx_vals)
        val = f"{val}, {extra_hx_val_str}"

    val = val + "}"

    return mark_safe(val)


@register.simple_tag(takes_context=True)
def get_input_value(
    context: Context, selected_options: list[dict[str, Any]] | None
) -> str:
    """Get the input display value for single-select mode.

    Args:
        context: The template context.
        selected_options: List of selected option dictionaries.

    Returns:
        The display value for the input.
    """
    if not selected_options:
        return ""

    ac_class: Any = context.get("ac_class")
    if ac_class is None:
        return ""

    return ac_class.get_input_value(
        selected_options[0]["key"], selected_options[0]["label"]
    )


@register.simple_tag(takes_context=True)
def get_chip_label(context: Context, selected_option: dict[str, Any] | None) -> str:
    """Get the chip display label for multi-select mode.

    Args:
        context: The template context.
        selected_option: Selected option dictionary.

    Returns:
        The chip display label.
    """
    if not selected_option:
        return ""

    ac_class: Any = context.get("ac_class")
    if ac_class is None:
        return ""

    return ac_class.get_chip_label(selected_option["key"], selected_option["label"])
