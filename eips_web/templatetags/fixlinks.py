import re

from django import template

register = template.Library()


@register.filter(name="fixlinks")
def fixlinks_filter(value: str):
    """Fix links in EIP docs to match our paths."""

    def fix_asset(matchobj: re.Match) -> str:
        return matchobj.group(0).replace("/assets/", "/static/assets/")

    def fix_link(matchobj: re.Match) -> str:
        return matchobj.group(0).replace(".md", ".html")

    fixed_links = re.sub(r"(eip|erc)\-[0-9]+.md", fix_link, value)
    fixed_assets = re.sub(r"/assets/", fix_asset, fixed_links)
    return fixed_assets
