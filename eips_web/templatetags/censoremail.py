import re

from django import template

register = template.Library()

EMAIL_REGEX = r"[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*"


@register.filter(name="censoremail")
def censoremail_filter(value: str):
    """Fix links in EIP docs to match our paths."""

    def hide_email(matchobj: re.Match) -> str:
        return matchobj.group(0).replace("@", " _at_ ")

    return re.sub(
        EMAIL_REGEX, hide_email, value.replace("<", "&lt;").replace(">", "&gt;")
    )
