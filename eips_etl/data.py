from dataclasses import dataclass
from typing import Any, Sequence

from django.db import models
from django.db.models import Q
from eips.enum import DocumentType

from eips_etl.models import Commit, Document

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
    document_id: str
    text: str

    @property
    def link(self) -> str:
        return f"/{self.document_type.lower()}s/{self.document_type.lower()}-{self.document_id}.html"


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
    doc_type: type[DocumentType], doc_id: int, commit: str | None = None
) -> Document | None:
    try:
        fkwargs = {
            "document_type": doc_type,
            "document_id": doc_id,
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
                AND sd.document_id = d.document_id
            )
        )
        WHERE d.document_type = '{doc_type.value}'
        ORDER BY c.commit_time DESC
        LIMIT 10
    """
    return Document.objects.raw(query)


def get_highlights() -> Sequence[Document]:
    where: models.QuerySet = Q()
    for doc_type, doc_id in HIGHLIGHTS:
        # where |= Document.objects.filter(document_id=doc_id, document_type=doc_type)
        where |= Q(document_id=doc_id, document_type=doc_type)

    highlights = []
    for doc in (
        Document.objects.filter(where).values("document_type", "document_id").distinct()
    ):
        text = f"{doc['document_type']}-{doc['document_id']}"
        highlights.append(
            Highlight(
                document_id=doc["document_id"],
                document_type=doc["document_type"],
                text=text,
            )
        )

    return highlights
