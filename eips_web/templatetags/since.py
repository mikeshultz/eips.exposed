from datetime import UTC, datetime

from django import template
from humanize.time import naturaldelta

register = template.Library()


@register.filter(name="since")
def since_filter(value: datetime) -> str:
    """Get a humanized duration since given tim."""
    now = datetime.now(tz=UTC)
    return naturaldelta(now - value)
