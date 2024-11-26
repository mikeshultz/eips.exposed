from django import template

register = template.Library()


@register.filter(name="decode")
def decode_filter(value: bytes):
    """Decode a utf-8 byte string."""
    return value.decode("utf-8")
