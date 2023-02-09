from django.template import loader
from django.http import HttpResponse

from . import ac_controls
from .forms import (
    SingleFormGetItem,
    SingleFormModel,
    MultipleFormGetItem,
    MultipleFormModel,
)


def index(request):
    print(request.POST)
    template = loader.get_template("index.html")
    single_form_get_item = SingleFormGetItem({"name": "Team Pickle", "company": [2]})
    single_form_model = SingleFormModel({"name": "Team Pickles", "members": [1]})
    multi_form_get_item = MultipleFormGetItem(
        {"name": "Team Pickle", "members": [1, 2, 3, 21]}
    )
    multi_form_model = MultipleFormModel(request.POST or None)
    return HttpResponse(
        template.render(
            {
                "single_form_model": single_form_model,
                "single_form_get_item": single_form_get_item,
                "multi_form_get_item": multi_form_get_item,
                "multi_form_model": multi_form_model,
            },
            request,
        )
    )
