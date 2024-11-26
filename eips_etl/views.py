from django.http import HttpRequest, HttpResponse


def stats(_request: HttpRequest) -> HttpResponse:
    return HttpResponse(b"Stats page")
