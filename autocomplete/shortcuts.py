import operator
from functools import reduce

from django.db.models import Q

from .core import Autocomplete


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
    def get_label_for_record(cls, record):
        return str(record)

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

        items = QuerysetMappedIterable(
            queryset=filtered_queryset, label_for_record=cls.get_label_for_record
        )
        return items

    @classmethod
    def get_items_from_keys(cls, keys, context):
        queryset = cls.get_queryset()
        results = queryset.filter(id__in=keys)

        return [
            {"key": record.id, "label": cls.get_label_for_record(record)}
            for record in results
        ]


class QuerysetMappedIterable:
    """
    We want to return an iterable of dicts rather than ORM records

    Using a list is inefficient for large datasets
    But using something like a generator/map doesn't allow for slicing or len()

    This class wraps a queryset's slice/len methods
    """

    def __init__(self, queryset, label_for_record):
        self.queryset = queryset
        self.label_for_record = label_for_record

    def __iter__(self, *args, **kwargs):
        return (self.map_record(r) for r in self.queryset)

    def map_record(self, record):
        return {"key": record.id, "label": self.label_for_record(record)}

    def __getitem__(self, key):
        # Handle both single index and slice objects
        if isinstance(key, int):
            records = [self.queryset[key]]
        elif isinstance(key, slice):
            records = self.queryset[key.start : key.stop : key.step]
        else:
            raise TypeError("Invalid argument type")

        mapped = [self.map_record(r) for r in records]

        if isinstance(key, int):
            return mapped[0]

        return mapped

    def __len__(self):
        # Return the length of the sequence
        return self.queryset.count()
