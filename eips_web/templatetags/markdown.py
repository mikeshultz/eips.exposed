from django import template
from django.utils.safestring import SafeString
from markdown import markdown

register = template.Library()


@register.filter(name="markdown")
def markdown_filter(value: str):
    """Render markdownt to HTML"""
    return SafeString(markdown(value, extensions=["fenced_code", "codehilite"]))
