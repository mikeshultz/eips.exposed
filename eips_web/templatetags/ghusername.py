import re

from django import template

register = template.Library()

GH_USERNAME_REGEX = (
    r"\(\B@([A-Za-z0-9](?:-(?=[A-Za-z0-9])|[A-Za-z0-9]){0,38}(?<=[A-Za-z0-9]))\)"
)


@register.filter(name="ghusername")
def ghusername_filter(value: str):
    """Make links to github usernames."""

    def link_username(matchobj: re.Match) -> str:
        username = matchobj.group(0)[2:-1]
        return f"([@{username}](https://github.com/{username}))"

    return re.sub(GH_USERNAME_REGEX, link_username, value)
