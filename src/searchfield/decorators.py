from __future__ import annotations

from typing import Callable, TypeVar

from .fields import SearchField

T = TypeVar("T")


def add_searchfield(**fields_config: list[str]) -> Callable[[type[T]], type[T]]:
    """Decorator to automatically add SearchField fields to a Django model.

    Each keyword argument maps a field name to its source_fields list.
    Example: @add_searchfield(search=['title', 'category']) adds a 'search' field.
    """

    def decorator(cls: type[T]) -> type[T]:
        for field_name, source_fields in fields_config.items():
            field = SearchField(source_fields=source_fields)
            cls.add_to_class(field_name, field)  # type: ignore[attr-defined]
        return cls

    return decorator
