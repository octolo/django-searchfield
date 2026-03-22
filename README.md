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

```bash
./service.py dev install-dev
./service.py dev test
```

## License

MIT
