from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Iterator, Sequence

from django.db import models
from django.db.models import Q
from eips.enum import DocumentType

from eips_etl.models import Commit, Document, DocumentError
from eips_web.object import SitemapURL

# Model prop filters
COMMIT_PROPS = [
    "commit_id",
    "author",
    "committer",
    "author_time",
    "commit_time",
    "gpg_sig",
    "message",
    "parents",
]
DOCUMENT_PROPS = [
    "document_id",
    "document_number",
    "commit",
    "document_type",
    "created",
    "updated",
    "status",
    "category",
    "type",
    "resolution",
    "title",
    "discussions_to",
    "review_period_end",
    "requires",
    "replaces",
    "superseded_by",
    "description",
    "body",
    "error_message",
]
# TODO: Generate these from metrics
HIGHLIGHTS = [
    (DocumentType.ERC, 20),
    (DocumentType.ERC, 721),
    (DocumentType.EIP, 1559),
    (DocumentType.ERC, 1155),
    (DocumentType.EIP, 7702),
    (DocumentType.EIP, 4484),
]


@dataclass
class Highlight:
    document_type: str
    document_number: str
    text: str

    @property
    def link(self) -> str:
        return f"/{self.document_type.lower()}s/{self.document_type.lower()}-{self.document_number}.html"


def dump_model(
    inst: models.Model, field_filter: list[str] | None = None
) -> dict[str, Any]:
    """Dump a flat model into a Python dict"""
    fields = field_filter if field_filter else [f.name for f in inst._meta.fields]
    return {k: v for k, v in inst.__dict__.items() if k in fields}


def get_commit(commit_id: str) -> Commit | None:
    try:
        return (
            Commit.objects.select_related("author")
            .select_related("committer")
            .filter(commit_id=commit_id)
            .order_by("-commit_time")
            .values(*COMMIT_PROPS, "committer__person_string", "author__person_string")
            .first()
        )
    except Commit.DoesNotExist:
        return None


def get_latest_commits(count: int) -> Sequence[Commit]:
    return Commit.objects.order_by("-commit_time").values(*COMMIT_PROPS)[:count]


def get_document(
    doc_type: type[DocumentType], doc_num: int, commit: str | None = None
) -> Document | None:
    try:
        fkwargs = {
            "document_type": doc_type,
            "document_number": doc_num,
        }

        if commit:
            fkwargs["commit_id"] = commit

        doc = (
            Document.objects.select_related("commit")
            .prefetch_related("authors")
            .filter(**fkwargs)
            .order_by("-commit__commit_time")
            .first()
        )
        # .values(*DOCUMENT_PROPS)

        if not doc:
            return None

        print("-doc:", doc)
        doc_dict = dump_model(doc)
        authors = doc.authors.all()
        print("-doc.authors:", doc.authors)
        print("-authors:", authors)
        doc_dict["authors"] = [a.person_string for a in authors]
        doc_dict["link"] = doc.link
        doc_dict["source_link"] = doc.source_link

        return doc_dict
    except Document.DoesNotExist:
        return None


def get_documents_by_commit(commit_id: str | None = None) -> Sequence[Document]:
    return (
        Document.objects.select_related("commit")
        .prefetch_related("authors")
        .filter(commit_id=commit_id)
        .order_by("-commit__commit_time")
    )


def get_popular_docs(doc_type: type[DocumentType], count: int) -> Sequence[Document]:
    query = f"""
        SELECT DISTINCT d.*, c.commit_time
        FROM eips_etl_document d
        JOIN eips_etl_commit c ON (
            c.commit_id = d.commit_id
            AND c.commit_time = (
                SELECT MAX(sc.commit_time)
                FROM eips_etl_commit sc
                JOIN eips_etl_document sd USING (commit_id)
                WHERE sd.document_type = d.document_type
                AND sd.document_number = d.document_number
            )
        )
        WHERE d.document_type = '{doc_type.value}'
        ORDER BY c.commit_time DESC
        LIMIT {count}
    """
    return Document.objects.raw(query)


def get_highlights() -> Sequence[Document]:
    where: models.QuerySet = Q()
    for doc_type, doc_num in HIGHLIGHTS:
        # where |= Document.objects.filter(document_number=doc_num, document_type=doc_type)
        where |= Q(document_number=doc_num, document_type=doc_type)

    highlights = []
    for doc in (
        Document.objects.filter(where)
        .values("document_type", "document_number")
        .distinct()
    ):
        text = f"{doc['document_type']}-{doc['document_number']}"
        highlights.append(
            Highlight(
                document_number=doc["document_number"],
                document_type=doc["document_type"],
                text=text,
            )
        )

    return highlights


def generate_sitemap() -> Iterator[SitemapURL]:
    latest_commits = get_latest_commits(1)
    if latest_commits:
        latest_commit_time = Commit.objects.order_by("-commit_time")[0].commit_time
    else:
        latest_commit_time = datetime.now(tz=UTC)

    # TODO: Include common search results
    yield SitemapURL(loc="/", priority="1.0", lastmod=latest_commit_time.isoformat())
    # yield SitemapURL(url=f"{base_url}/search.html", priority=0.8),
    yield SitemapURL(
        loc="/index.html",
        priority="0.9",
        lastmod=latest_commit_time.isoformat(),
    )

    def makeurl(doc: Document) -> SitemapURL:
        return SitemapURL(
            loc=doc.link,
            priority="0.7",
            lastmod=doc.commit.commit_time.isoformat(),
        )

    for doc_type in [DocumentType.EIP, DocumentType.ERC]:
        for doc in get_popular_docs(doc_type, 10_000):
            yield makeurl(doc)

    for commit in Commit.objects.order_by("-commit_time").all():
        yield SitemapURL(
            loc=commit.link,
            priority="0.4",
            lastmod=commit.commit_time.isoformat(),
        )


def get_errors_paginated(page: int = 1, count: int = 100):
    return (
        DocumentError.objects.select_related("document")
        .select_related("document__commit")
        .order_by("-document__commit__commit_time", "-document__updated")[
            count * (page - 1) : count * page
        ]
    )
