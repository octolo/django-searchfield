from __future__ import annotations

import re
import unicodedata
from datetime import date, datetime
from typing import Any

from django.db import models


def get_value_by_path(obj: Any, path: str, default: Any = None) -> Any:
    """
    Resolve a dotted path on an object.
    Supports: object attributes (contact.lastname), dict/JSON keys (data.firstname), list indices (items.0).
    """
    if not path:
        return default
    current = obj
    for key in path.split("."):
        if current is None:
            return default
        try:
            if isinstance(current, dict):
                current = current.get(key)
            elif hasattr(current, key):
                current = getattr(current, key)
            elif key.isdigit():
                idx = int(key)
                current = current[idx] if idx < len(current) else None
            else:
                return default
        except (KeyError, AttributeError, TypeError, IndexError):
            return default
    return current


def make_searchable(
    input_str: str,
    replace_chars: list[str] | None = None,
) -> str:
    """
    Normalize string for search: replace separators with space, NFKD, remove combining chars, lowercase.
    """
    if input_str is None:
        return ""
    s = str(input_str)
    for char in replace_chars or ["_", ";", ","]:
        s = s.replace(char, " ")
    s = re.sub(r" +", " ", s)
    nfkd = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in nfkd if not unicodedata.combining(c))
    return s.lower()


class SearchField(models.TextField):
    """
    Field that concatenates multiple source paths into a search-indexed string.
    Uses '_' by default for simple startswith/contains queries.
    Source paths support dotted notation: 'name', 'contact.lastname', 'contact_data.firstname' (JSON).
    Not unique by default (allows homonyms); pass unique=True to enforce uniqueness.
    """

    def __init__(
        self,
        source_fields: list[str],
        separator: str = "_",
        replace_chars: list[str] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.source_fields = source_fields
        self.separator = separator
        self.replace_chars = replace_chars or ["_", ";", ","]
        kwargs.setdefault("editable", False)
        kwargs.setdefault("blank", True)
        kwargs.setdefault("null", True)
        kwargs.setdefault("db_index", True)
        kwargs.setdefault("unique", False)  # Allow homonyms by default
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance: Any, add: bool) -> str | None:
        values = self._collect_values(model_instance)
        if not values:
            return None
        return self.separator.join(values)

    def _collect_values(self, model_instance: Any) -> list[str]:
        """Get and normalize values from source paths, concatenate with separator.
        Duplicates are removed while preserving source order."""
        result = []
        seen: set[str] = set()
        for path in self.source_fields:
            value = get_value_by_path(model_instance, path)
            if value is not None and value != "":
                formatted = self._format_value(value)
                if formatted and formatted not in seen:
                    seen.add(formatted)
                    result.append(formatted)
        return result

    def _format_value(self, value: Any) -> str:
        """Format value for search: lowercase, alphanumeric + separator only."""
        if isinstance(value, (date, datetime)):
            s = value.strftime("%Y%m%d")
        elif isinstance(value, (int, float)):
            s = str(value)
        elif isinstance(value, bool):
            s = "1" if value else "0"
        else:
            s = str(value)
        s = make_searchable(s, replace_chars=self.replace_chars)
        s = s.replace(" ", self.separator)
        s = re.sub(r"[^\w" + re.escape(self.separator) + r"]", "", s)
        s = re.sub(rf"{re.escape(self.separator)}+", self.separator, s)
        return s.strip(self.separator)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["source_fields"] = self.source_fields
        if self.separator != "_":
            kwargs["separator"] = self.separator
        if self.replace_chars != ["_", ";", ","]:
            kwargs["replace_chars"] = self.replace_chars
        if self.unique:
            kwargs["unique"] = True
        return name, path, args, kwargs
