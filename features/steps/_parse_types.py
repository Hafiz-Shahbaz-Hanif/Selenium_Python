"""Custom ``parse`` types, registered before any step module that uses them.

Behave imports the modules in ``features/steps/`` in filename order, and this
file sorts first, so ``{x:Optional}`` is available everywhere.
"""
import parse
from behave import register_type


@parse.with_pattern(r'[^"]*')
def parse_optional(text: str) -> str:
    """A quoted value that is allowed to be empty (``""``)."""
    return text


register_type(Optional=parse_optional)
