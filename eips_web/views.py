from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from eips.enum import DocumentType, EIP1Status
from typesense.exceptions import ObjectNotFound

from eips_etl.data import (
    get_commit,
    get_document,
    get_documents_by_commit,
    get_errors_paginated,
    get_highlights,
    get_latest_commits,
    get_popular_docs,
)
from eips_etl.models import Commit, DocumentError, Sitemap
from eips_etl.search import search
from eips_web.util import exctract_move_dest


def index_html(request: HttpRequest) -> HttpResponse:
    commits = get_latest_commits(20)
    eips = get_popular_docs(DocumentType.EIP, 10)
    ercs = get_popular_docs(DocumentType.ERC, 10)
    highlights = get_highlights()
    return render(
        request,
        "index.html",
        context=dict(
            commits=commits,
            eips=eips,
            ercs=ercs,
            highlights=highlights,
        ),
    )


def search_html(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        return render(
            request,
            "http_error.html",
            {"http_status": 405, "error": "Method Not Allowed"},
            status=405,
        )

    q = request.GET.get("q")
    page: int = 1
    try:
        page = int(request.GET.get("p", "1"))
    except ValueError:
        pass

    if not isinstance(page, str):
        return render(
            request,
            "http_error.html",
            {"http_status": 400, "error": "Invalid Page"},
            status=400,
        )

    try:
        doc_hits, commit_hits = search(q, page)
    except ObjectNotFound:
        return render(
            request,
            "http_error.html",
            {"http_status": 503, "error": "Search currently unavailable."},
            status=503,
        )

    return render(
        request,
        "search.html",
        context=dict(
            q=q,
            doc_hits=doc_hits,
            commit_hits=commit_hits,
        ),
    )


def search_json(request: HttpRequest) -> HttpResponse:
    return JsonResponse({"result": []})


def eip_html(request: HttpRequest, doc_id: int) -> HttpResponse:
    if doc := get_document(DocumentType.EIP, doc_id):
        if doc.get("status") == EIP1Status.MOVED:
            if dest := exctract_move_dest(doc["body"]):
                return redirect(dest, permanent=True)

        return render(
            request,
            "document.html",
            context=dict(**doc),
        )

    return render(
        request,
        "http_error.html",
        {"http_status": 404, "error": "Document Not Found"},
        status=404,
    )


def eip_json(request: HttpRequest, doc_id: int) -> HttpResponse:
    if doc := get_document(DocumentType.EIP, doc_id):
        if doc.get("status") == EIP1Status.MOVED:
            if dest := exctract_move_dest(doc["body"]):
                return redirect(dest, permanent=True)
        return JsonResponse(doc)
    return JsonResponse({"error": "Document Not Found"}, status=404)


def erc_html(request: HttpRequest, doc_id: int) -> HttpResponse:
    if doc := get_document(DocumentType.ERC, doc_id):
        if doc.get("status") == EIP1Status.MOVED:
            if dest := exctract_move_dest(doc["body"]):
                return redirect(dest, permanent=True)
        return render(
            request,
            "document.html",
            context=dict(**doc),
        )

    return render(
        request,
        "http_error.html",
        {"http_status": 404, "error": "Document Not Found"},
        status=404,
    )


def erc_json(request: HttpRequest, doc_id: int) -> HttpResponse:
    if doc := get_document(DocumentType.ERC, doc_id):
        if doc.get("status") == EIP1Status.MOVED:
            if dest := exctract_move_dest(doc["body"]):
                return redirect(dest, permanent=True)
        return JsonResponse(doc)
    return JsonResponse({"error": "Document Not Found"}, status=404)


def commit_html(request: HttpRequest, commit_id: str) -> HttpResponse:
    if commit := get_commit(commit_id):
        docs = get_documents_by_commit(commit_id)

        if docs:
            document_type = docs[0].document_type
        else:
            document_type = "EIP"

        return render(
            request,
            "commit.html",
            context=dict(
                **commit,
                docs=docs,
                document_type=document_type,
            ),
        )

    return render(
        request,
        "http_error.html",
        {"http_status": 404, "error": "Commit Not Found"},
        status=404,
    )


def commit_json(request: HttpRequest, commit_id: str) -> HttpResponse:
    return JsonResponse(
        Commit.objects.filter(commit_id=commit_id)
        .order_by("-created")
        .values(COMMIT_PROPS)
        .first()
    )


def parse_errors_html(request: HttpRequest) -> HttpResponse:
    try:
        page = int(request.GET.get("p", "1"))
    except ValueError:
        page = 1

    page_size = 100
    count = DocumentError.objects.count()
    pages = count // page_size
    errors = get_errors_paginated(page, page_size)

    return render(
        request,
        "parse-errors.html",
        context=dict(
            page=page,
            pages=pages,
            errors=errors,
        ),
    )


def health_json(request: HttpRequest) -> HttpResponse:
    return JsonResponse({"healthy": True})


def sitemap_xml(request: HttpRequest) -> HttpResponse:
    sitemap = Sitemap.objects.order_by("-generation_time").first()

    if not sitemap:
        return render(
            request,
            "http_error.html",
            {"http_status": 404, "error": "Sitemap not yet generated"},
            status=404,
        )

    return HttpResponse(sitemap.xml_data, content_type="text/xml")


def deprecated_eip_redirect(request: HttpRequest, doc_id: int) -> HttpResponse:
    return redirect(f"/eips/eip-{doc_id}.html", permanent=True)


def deprecated_erc_redirect(request: HttpRequest, doc_id: int) -> HttpResponse:
    return redirect(f"/ercs/erc-{doc_id}.html", permanent=True)
