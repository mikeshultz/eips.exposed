from django.http import HttpResponse


def stats(_request) -> HttpResponse:
    return HttpResponse(b"Stats page")
