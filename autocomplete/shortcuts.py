import operator
from functools import reduce

from django.db.models import Q

from .autocomplete import Autocomplete


class ModelAutocomplete(Autocomplete):
    model = None
    search_attrs = []

    @classmethod
    def get_search_attrs(cls):
        if not cls.search_attrs:
            raise ValueError("ModelAutocomplete must have search_attrs")
        return cls.search_attrs

    @classmethod
    def get_model(cls):
        if not cls.model:
            raise ValueError("ModelAutocomplete must have a model")

        return cls.model

    @classmethod
    def get_queryset(cls):
        return cls.get_model().objects.all()

    @classmethod
    def get_query_filtered_queryset(cls, search, context):
        base_qs = cls.get_queryset()
        conditions = [
            Q(**{f"{attr}__icontains": search}) for attr in cls.get_search_attrs()
        ]
        condition_filter = reduce(operator.or_, conditions)
        queryset = base_qs.filter(condition_filter)
        return queryset

    @classmethod
    def search_items(cls, search, context):
        filtered_queryset = cls.get_query_filtered_queryset(search, context)

        paged_records = filtered_queryset[: cls.max_results]
        items = [{"key": obj.id, "label": str(obj)} for obj in paged_records]
        return items

    @classmethod
    def get_items_from_keys(cls, keys, context):
        queryset = cls.get_queryset()
        results = queryset.filter(id__in=keys)
        return [{"key": person.id, "label": person.name} for person in results]
