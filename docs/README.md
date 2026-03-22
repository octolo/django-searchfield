## Assistant Guidelines

This file provides general guidelines for the AI assistant working on this project.

For detailed information, refer to:
- `AI.md` - Condensed reference guide for AI assistants (start here)
- `purpose.md` - Project purpose and goals
- `structure.md` - Project structure and module organization
- `development.md` - Development guidelines and best practices

### Quick Reference

- Always use `./service.py dev <command>` or `python service.py dev <command>` for project tooling
- Always use `./service.py quality <command>` or `python service.py quality <command>` for quality checks
- Always use `./service.py django <command>` or `python service.py django <command>` for Django commands
- Maintain clean module organization and separation of concerns
- Default to English for all code artifacts (comments, docstrings, logging, error strings, documentation snippets, etc.)
- Follow Python best practices and quality standards
- Keep dependencies minimal and prefer standard library
- Ensure all public APIs have type hints and docstrings
- Write tests for new functionality
- Source code in `src/` directory

### Django SearchField-Specific Guidelines

- **Field development**: SearchField is read-only; unique=False by default (homonyms allowed)
- **Decorator development**: The add_searchfield decorator should add fields dynamically to models
- **Duplicate removal**: Duplicate values from source fields are removed before concatenation
- **Value generation**: Values must be generated automatically before saving

### Field Implementation Checklist

When working with SearchField:
- [ ] Field is not unique by default (`unique=False`); pass unique=True if needed
- [ ] Field is optional (`blank=True`, `null=True`)
- [ ] Field is always read-only (`editable=False`)
- [ ] Values are generated in `pre_save()`
- [ ] Duplicates from source fields are removed before concatenation
- [ ] Source fields are properly formatted (dates, numbers, etc.)

### Decorator Implementation Checklist

When working with add_searchfield decorator:
- [ ] Decorator accepts keyword arguments (field_name: list of source fields)
- [ ] Fields are added using `add_to_class()`
- [ ] All fields have appropriate defaults (max_length, etc.)
