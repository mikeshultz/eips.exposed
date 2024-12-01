import re

from django import template

register = template.Library()


@register.filter(name="fixlinks")
def fixlinks_filter(value: str):
    """Fix links in EIP docs to match our paths."""

    def fix_asset(matchobj: re.Match) -> str:
        return matchobj.group(0).replace("/assets/", "/static/assets/")

    def fix_link(matchobj: re.Match) -> str:
        matched = matchobj.group(0)

        # NOTE: This is kind of a circuit breaker indicating it matched part of
        #       a full URL.
        # TODO: Make this more robust. Maybe update the regex to negative
        #       lookbehind for http://?
        if matched.startswith("/"):
            return matched

        if matched.startswith("./"):
            matched = matched.replace("./", "")

        if matchobj.group(1) == "erc":
            prefix = "/ercs/"
        else:
            prefix = "/eips/"

        rewrite = matched.replace(".md", ".html")
        fin = f"{prefix}{rewrite}"
        return fin

    # (?<!http:\/\/)
    fixed_links = re.sub(r"[\./]*(eip|erc)\-[0-9]+.md", fix_link, value)
    fixed_assets = re.sub(r"/assets/", fix_asset, fixed_links)
    return fixed_assets
