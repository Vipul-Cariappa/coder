from django import template
from django.utils.safestring import mark_safe

from challenges.functions import sanitize

register = template.Library()


@register.filter(name="safe_html")
def safe_html(value):
    """Render stored HTML after stripping anything that could execute.

    Use this instead of ``|safe`` for user supplied content. Rows written
    before rendering was sanitized are cleaned on the way out, so no data
    migration is needed.
    """
    return mark_safe(sanitize(value or ""))
