"""
Django template tags to facilitate rendering of the component
"""
import hashlib

from django import template
from django import urls
from django.utils.html import format_html
from django.utils.http import urlencode
from django.template import loader
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def make_id(value):
    """Generate an ID given a string, to use as element IDs in HTML"""
    return hashlib.sha1(value.encode('utf-8')).hexdigest()

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
    options_selected = ','.join(
        [str(x) for x in selected]) if selected is not None else ''

    url = urls.reverse(name, kwargs={'method': 'component'})
    parameter = urlencode({name: options_selected})
    get_url = f"{url}?{parameter}"

    return format_html((
        "<div "
            f"hx-get=\"{get_url}\""
            "hx-trigger=\"load\""
            "hx-swap=\"outerHTML\">"
        "</div>"
    ))


@register.simple_tag
def autocomplete_head(bootstrap=False):
    """
    Renders the styles required for the component

    Parameters:

        bootstrap   Set to true if the bootstrap css should be loaded from cdn
                    Defaults to False.
    """
    return loader.get_template('autocomplete/head.html', using="django").render(
        {'bootstrap': bootstrap}
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
    return loader.get_template('autocomplete/scripts.html', using="django"). \
        render({
            'csrf_token': context.get('csrf_token', ''),
            'bootstrap': bootstrap,
            'htmx': htmx,
            'htmx_csrf': htmx_csrf,
        }
    )
