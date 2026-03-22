## Project Purpose

**Django SearchField** is a Django library that provides a field type for automatically generating concatenated values by combining multiple model fields for full-text search.

### Core Functionality

The library enables you to:

1. **Create concatenated values** by combining multiple fields:
   - Automatically generate values from source fields (e.g., `name`, `id`, `date`)
   - Format values appropriately (dates as `YYYYMMDD`, numbers as strings, etc.)
   - Remove duplicate values before concatenation

2. **SearchField**:
   - Automatically generates values before saving
   - Read-only (cannot be edited)
   - Not unique by default (allows homonyms)

3. **Decorator support**:
   - Use `@add_searchfield()` decorator to automatically add multiple SearchField fields
   - Define multiple fields at once with different source field combinations

### Architecture

The library provides:

- **`SearchField`**: A Django CharField that combines multiple source fields into a search-indexed string
- **`add_searchfield`**: A decorator to automatically add SearchField instances to models

### Use Cases

- Concatenate multiple fields for search (startswith/icontains)
- Allow homonyms by default (no unique constraint)
- Create composite search strings for contacts, names, products, etc.
