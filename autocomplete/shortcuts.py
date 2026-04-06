"""Shortcuts for common autocomplete implementations.

Provides ModelAutocomplete for easy integration with Django models.
"""

import operator
from collections.abc import Callable, Iterable, Iterator
from functools import reduce
from typing import TYPE_CHECKING, Any

from django.db.models import Q, Model, QuerySet

from autocomplete.core import Autocomplete, ContextArg


class ModelAutocomplete(Autocomplete):
    """Autocomplete implementation for Django models.

    This class provides a ready-to-use autocomplete that searches
    and retrieves items from a Django model.

    Attributes:
        model: The Django model class to use.
        search_attrs: List of model attributes to search in.
    """

    model: type[Model] | None = None
    search_attrs: list[str] = []

    @classmethod
    def get_search_attrs(cls) -> list[str]:
        """Get the list of model attributes to search.

        Returns:
            List of attribute names.

        Raises:
            ValueError: If search_attrs is not defined.
        """
        if not cls.search_attrs:
            raise ValueError("ModelAutocomplete must have search_attrs")
        return cls.search_attrs

    @classmethod
    def get_model(cls) -> type[Model]:
        """Get the Django model class.

        Returns:
            The model class.

        Raises:
            ValueError: If model is not defined.
        """
        if not cls.model:
            raise ValueError("ModelAutocomplete must have a model")

        return cls.model

    @classmethod
    def get_queryset(cls) -> QuerySet:
        """Get the base queryset for the model.

        Returns:
            QuerySet of all model instances.
        """
        return cls.get_model().objects.all()

    @classmethod
    def get_label_for_record(cls, record: Model) -> str:
        """Get the display label for a model instance.

        Args:
            record: The model instance.

        Returns:
            The string representation of the record.
        """
        return str(record)

    @classmethod
    def get_query_filtered_queryset(cls, search: str, context: ContextArg) -> QuerySet:
        """Filter the queryset based on the search query.

        Args:
            search: The search query string.
            context: The context containing request information.

        Returns:
            Filtered QuerySet.
        """
        base_qs: QuerySet = cls.get_queryset()
        conditions: list[Q] = [
            Q(**{f"{attr}__icontains": search}) for attr in cls.get_search_attrs()
        ]
        condition_filter: Q = reduce(operator.or_, conditions)
        queryset: QuerySet = base_qs.filter(condition_filter)
        return queryset

    @classmethod
    def search_items(cls, search: str, context: ContextArg) -> Iterable[dict[str, Any]]:
        """Search for model instances matching the query.

        Args:
            search: The search query string.
            context: The context containing request information.

        Returns:
            Iterable of item dictionaries.
        """
        filtered_queryset: QuerySet = cls.get_query_filtered_queryset(search, context)

        items: QuerysetMappedIterable = QuerysetMappedIterable(
            queryset=filtered_queryset,
            label_for_record=cls.get_label_for_record,
        )
        return items

    @classmethod
    def get_items_from_keys(
        cls, keys: Iterable[str | int], context: ContextArg | None
    ) -> list[dict[str, Any]]:
        """Get model instances by their primary keys.

        Args:
            keys: Iterable of primary keys.
            context: The context containing request information, or None.

        Returns:
            List of item dictionaries.
        """
        queryset: QuerySet = cls.get_queryset()
        results: QuerySet = queryset.filter(id__in=keys)

        return [
            {"key": record.id, "label": cls.get_label_for_record(record)}
            for record in results
        ]


class QuerysetMappedIterable:
    """Lazy iterable that maps queryset results to dictionaries.

    We want to return an iterable of dicts rather than ORM records.

    Using a list is inefficient for large datasets.
    But using something like a generator/map doesn't allow for slicing or len().

    This class wraps a queryset's slice/len methods.

    Attributes:
        queryset: The underlying Django QuerySet.
        label_for_record: Callable to get label from a record.
    """

    def __init__(
        self,
        queryset: QuerySet,
        label_for_record: Callable[[Model], str],
    ) -> None:
        """Initialize the iterable.

        Args:
            queryset: The queryset to iterate over.
            label_for_record: Function to get label from record.
        """
        self.queryset: QuerySet = queryset
        self.label_for_record: Callable[[Model], str] = label_for_record

    def __iter__(self) -> Iterator[dict[str, Any]]:
        """Return an iterator over mapped records.

        Returns:
            Generator yielding item dictionaries.
        """
        return (self.map_record(r) for r in self.queryset)

    def map_record(self, record: Model) -> dict[str, Any]:
        """Map a model record to an item dictionary.

        Args:
            record: The model instance.

        Returns:
            Item dictionary with key and label.
        """
        return {"key": record.id, "label": self.label_for_record(record)}

    def __getitem__(self, key: int | slice) -> dict[str, Any] | list[dict[str, Any]]:
        """Get item(s) by index or slice.

        Args:
            key: Index or slice to retrieve.

        Returns:
            Single item dict or list of item dicts.

        Raises:
            TypeError: If key is not int or slice.
        """
        # Handle both single index and slice objects
        if isinstance(key, int):
            records: list[Model] | QuerySet = [self.queryset[key]]
        elif isinstance(key, slice):
            records = self.queryset[key.start : key.stop : key.step]
        else:
            raise TypeError("Invalid argument type")

        mapped: list[dict[str, Any]] = [self.map_record(r) for r in records]

        if isinstance(key, int):
            return mapped[0]

        return mapped

    def __len__(self) -> int:
        """Return the count of items in the queryset.

        Returns:
            The queryset count.
        """
        return self.queryset.count()
