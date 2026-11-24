# django-searchfield

Django field that concatenates multiple fields into a search-indexed string.

## Purpose

Create a full-text search field by combining multiple model fields. Values are concatenated with `_` by default for simple `startswith` / `icontains` queries.

## Installation

```bash
pip install django-searchfield
```

## Quick Start

### Using SearchField directly

```python
from django.db import models
from searchfield import SearchField

class Product(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField()
    created_date = models.DateField()

    search = SearchField(source_fields=["name", "code", "created_date"])
```

### Using the decorator

```python
from django.db import models
from searchfield import add_searchfield

@add_searchfield(search=["title", "category"])
class Article(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    content = models.TextField()
```

### Path resolution (relations, JSON)

```python
class Creditor(models.Model):
    contact = models.ForeignKey(Contact, ...)
    contact_data = models.JSONField()  # {"firstname": "...", "lastname": "..."}

    search = SearchField(source_fields=[
        "name",
        "contact.lastname",       # relation
        "contact_data.firstname", # JSON keys
    ])
```

## Features

- **Automatic generation**: Values are generated automatically before saving
- **Path resolution**: Source paths support dotted notation (`name`, `contact.lastname`, `contact_data.firstname` for JSON)
- **Search indexing**: Normalized values (NFKD, lowercase) concatenated with `_` for `startswith`/`icontains`
- **Duplicate removal**: Duplicate values from source fields are removed before concatenation
- **Type formatting**: Automatically formats dates, numbers, booleans
- **Read-only**: Field is editable=False
- **db_index=True**: Indexed for search performance
- **unique=False**: Not unique by default (allows homonyms); pass unique=True to enforce

## Field Properties

- `editable=False`: Read-only
- `blank=True`, `null=True`: Optional (empty if all source fields are empty)
- `db_index=True`: Indexed for search queries
- `unique=False`: Homonyms allowed by default

## Development

CI runs the Django system check across the Python/Django matrix, Ruff, Bandit
(medium/high confidence and severity), runtime dependency advisories, and package
builds. It warns until an automated test suite is added.

```bash
./service.py dev install-dev
./service.py dev test
```

## License

MIT

## CI packaging check

CI also installs the built wheel(s) in a clean environment and checks their
dependencies and imports without publishing. This installation check is
non-blocking during the initial rollout.

## Local audit

Install the project's development/test dependencies (including both local
packages where applicable), plus the audit tools:

```bash
python -m pip install ruff mypy bandit pip-audit vulture radon xenon pytest pytest-django pytest-cov build twine
make audit
```

Use the activated environment's Python, or pass `make audit PYTHON=/path/to/python`.
On systems without Make, run `python scripts/audit.py` directly. Git is required;
the geoaddress widget tests also require Node.js. The audit reports missing test
suites and runs all available checks even when earlier checks fail.
Xenon checks the absolute C, module B, and average A complexity thresholds. Existing
lint, typing, security, dependency, or test findings can make the audit fail.
CI also runs this audit as a non-blocking job and separately reports Radon maintainability without imposing a threshold.
