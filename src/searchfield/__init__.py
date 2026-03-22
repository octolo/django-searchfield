"""Django SearchField - Field that combines multiple fields into a concatenated value."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("django-searchfield")
except PackageNotFoundError:
    __version__ = "0.0.0"

from .decorators import add_searchfield
from .fields import SearchField, make_searchable

__all__ = [
    "SearchField",
    "add_searchfield",
    "make_searchable",
]
