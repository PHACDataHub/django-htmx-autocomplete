from bs4 import BeautifulSoup
from django.http import QueryDict
from django.test.client import MULTIPART_CONTENT, Client


def get_soup(response):
    content = response.content
    return soup_from_str(content)


def soup_from_str(content):
    soup = BeautifulSoup(content, "html.parser")
    return soup


def put_request_as_querystring(client, url, data):
    """
    for some reason,
    htmx sends PUT requests as querystings??
    """
    qs = QueryDict(mutable=True)
    for k, v in data.items():
        if isinstance(v, list):
            qs.setlist(k, v)
        else:
            qs.update({k: v})

    query_string = qs.urlencode()
    response = client.put(url, data=query_string)
    return response
