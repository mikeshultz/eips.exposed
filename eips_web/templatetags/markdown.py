from io import StringIO

from django import template
from django.utils.safestring import SafeString
from markdown import Markdown, markdown

register = template.Library()

SKIP_TAGS = ["h1", "h2", "h3", "h4", "h5"]


def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text and element.tag not in SKIP_TAGS:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


# Ref: https://stackoverflow.com/a/54923798/402412
Markdown.output_formats["plain"] = unmark_element  # pyright: ignore
__md = Markdown(output_format="plain")  # pyright: ignore
__md.stripTopLevelTags = False


@register.filter(name="markdown")
def markdown_filter(value: str):
    """Render markdownt to HTML"""
    return SafeString(
        markdown(value, extensions=["fenced_code", "codehilite", "tables"])
    )


@register.filter(name="markdowntext")
def markdowntext_filter(value: str):
    """Render markdownt to plaintext"""
    return __md.convert(value)


@register.filter(name="markdownsnippet")
def markdownsnippet_filter(value: str, arg: str):
    """Render markdownt to plaintext snippet"""
    return " ".join(__md.convert(value).replace("\n", " ").split(" ")[: int(arg)])
