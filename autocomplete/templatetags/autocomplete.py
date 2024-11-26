"""
Django template tags to facilitate rendering of the component
"""

import hashlib
import json

from django import template, urls
from django.template import loader
from django.template.defaultfilters import stringfilter
from django.utils.html import escape, format_html
from django.utils.http import urlencode
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
@stringfilter
def make_id(value):
    """Generate an ID given a string, to use as element IDs in HTML"""
    return hashlib.sha1(value.encode("utf-8")).hexdigest()


@register.filter()
@stringfilter
def search_highlight(value, search):
    """Surround the section of text matching the search with a classed span"""
    if search == "":
        return value
    try:
        pos = value.lower().index(search.lower())
        start = escape(value[:pos])
        match = escape(value[pos : pos + len(search)])
        end = escape(value[pos + len(search) :])
        return mark_safe(f'{start}<span class="highlight">{match}</span>{end}')
    except ValueError:
        pass
    return value


@register.simple_tag(takes_context=True)
def use_string(context, name, strings):
    """
    Loads the string from a template or via the variable dict `strings` if the `name`
    key is defined within.  This allows strings to be overriden in 2 ways, either by
    user defined templates which will override *all* instances, or via the
    `custom_strings` property of the Autocomplete instance which allows individual
    customization.

    When `name` is not found in `strings`, the template name becomes:

    autocomplete/strings/{name}.html

    """
    if name in strings:
        return strings[name]

    return loader.get_template(
        f"autocomplete/strings/{name}.html", using="django"
    ).render(context.flatten())


@register.simple_tag
def substitute_string(template_str, **kwargs):
    """
    Substitute the template string with the kwargs
    """
    as_strings = {k: str(v) for k, v in kwargs.items()}
    return template_str % as_strings


@register.simple_tag
def autocomplete(name, selected=None):
    """
    Tag used to render autocomplete component in a Django Template

    Parameters:

        name        Name of the component.
                    The name is used to generate routes and must be unique.
                    Required.

        selected    Comma separated list of selected values
                    Defaults to None

    """
    options_selected = (
        ",".join([str(x) for x in selected]) if selected is not None else ""
    )

    url = urls.reverse(name, kwargs={"method": "component"})
    parameter = urlencode({name: options_selected})
    get_url = f"{url}?{parameter}"

    return format_html(
        (
            "<div "
            f'hx-get="{get_url}"'
            'hx-trigger="load"'
            'hx-swap="outerHTML">'
            "</div>"
        )
    )


@register.filter
def js_boolean(value):
    """
    Convert the value to a javascript boolean
    """
    return "true" if value else "false"


@register.simple_tag
def autocomplete_head(bootstrap=False):
    """
    Renders the styles required for the component

    Parameters:

        bootstrap   Set to true if the bootstrap css should be loaded from cdn
                    Defaults to False.
    """
    return loader.get_template("autocomplete/head.html", using="django").render(
        {"bootstrap": bootstrap}
    )


@register.simple_tag(takes_context=True)
def autocomplete_scripts(context, bootstrap=False, htmx=False, htmx_csrf=False):
    """
    Renders the required script tags for the component

    Parameters:

        bootstrap   Set to true if bootstrap should be loaded from cdn
                    Defaults to False.

        htmx        Set to true if htmx should be loaded from cdn
                    Defaults to False.

        htmx_csrf   Set to true if htmx should be initialized with csrf token
                    Defaults to False.

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
def value_if_truthy(test, value, default=""):
    """
    Return the value if it is truthy, otherwise return the default
    """
    return value if test else default


@register.simple_tag(takes_context=True)
def base_configurable_values_hx_params(context):

    field_name = context.get("field_name")
    required = context.get("required")
    disabled = context.get("disabled")
    placeholder = context.get("placeholder")
    multiselect = context.get("multiselect")

    hx_params = f"{field_name},field_name,item,component_prefix"

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
def base_configurable_hx_vals(context):
    """
    json-like format
    must be wrapped in curly braces
    """

    field_name = context.get("field_name")
    required = context.get("required")
    disabled = context.get("disabled")
    placeholder = context.get("placeholder")
    multiselect = context.get("multiselect")
    component_prefix = context.get("component_prefix")

    props = {
        "field_name": escape(field_name),
        "component_prefix": component_prefix,
    }

    if required:
        props["required"] = bool(required)

    if disabled:
        props["disabled"] = bool(disabled)

    if multiselect:
        props["multiselect"] = bool(multiselect)

    if placeholder:
        props["placeholder"] = escape(str(placeholder))

    hx_vals = json.dumps(props).replace("{", "").replace("}", "")

    return mark_safe(hx_vals)


def stringify_extra_hx_vals(extra_hx_vals_dict):
    if any("'" in val for val in extra_hx_vals_dict.values()):
        raise ValueError(
            "Extra hx vals cannot contain single quotes, consider backticks for JS expressions or escaping double-quotes"
        )

    return ",".join([f' "{key}": {val}' for key, val in extra_hx_vals_dict.items()])


@register.simple_tag(takes_context=True)
def text_input_hx_vals(context):
    """
    items has augments hx-vals,
    - it adds JS value of the search input
    - users can add more values in their class
    """

    base_hx_vals_str = base_configurable_hx_vals(context)

    component_id_escape = escape(context.get("component_id"))

    val = (
        "js:{"
        f"{base_hx_vals_str},"
        f'search: document.getElementById("{component_id_escape}__textinput").value'
    )

    extra_hx_vals = context.get("ac_class").get_extra_text_input_hx_vals()
    if extra_hx_vals:
        extra_hx_val_str = stringify_extra_hx_vals(extra_hx_vals)
        val = f"{val}, {extra_hx_val_str}"

    val = val + "}"

    return mark_safe(val)
