import os
from dataclasses import dataclass

import typesense

TYPESENSE_HOST = os.environ.get("TYPESENSE_HOST", "localhost")
TYPESENSE_PORT = os.environ.get("TYPESENSE_PORT", "8108")
TYPESENSE_API_KEY = os.environ.get("TYPESENSE_API_KEY", "asdf1234")

client: typesense.Client | None = None


@dataclass
class DocumentHit:
    document_type: str
    document_number: int
    link: str
    title: str
    snippet: str


@dataclass
class CommitHit:
    commit_id: int
    link: str
    title: str
    snippet: str


def _client(
    host: str = TYPESENSE_HOST,
    port: int = int(TYPESENSE_PORT),
    api_key: str = TYPESENSE_API_KEY,
) -> typesense.Client:
    global client

    if not client:
        client = typesense.Client(
            {
                "nodes": [{"host": host, "port": port, "protocol": "http"}],
                "api_key": api_key,
                "connection_timeout_seconds": 3,
            }
        )

    return client


def search(query: str, page: int = 1) -> tuple[list[DocumentHit], list[CommitHit]]:
    results = _client().multi_search.perform(
        {
            "searches": [
                {
                    "collection": "document",
                    "q": query,
                    "query_by": "document_number_string,document_type,title,description,commit,status,category,type,body",
                    "sort_by": "_text_match:desc,updated:desc,created:desc",
                    "group_by": "document_type,document_number",
                    "group_limit": 1,
                    # "facet_by": "document_type,type",
                    "page": page,
                    "per_page": 20,
                },
                {
                    "collection": "commit",
                    "q": query,
                    "query_by": "commit_id,message,author,committer",
                    "sort_by": "_text_match:desc,commit_time:desc,author_time:desc",
                    "page": page,
                    "per_page": 20,
                },
            ]
        },
        {
            "highlight_start_tag": "",
            "highlight_end_tag": "",
        },
    )

    docs: list[DocumentHit] = []
    commits: list[CommitHit] = []

    # docs
    for group in results["results"][0].get("grouped_hits", []):
        document_type = group["group_key"][0]
        document_number = group["group_key"][1]
        for hit in group.get("hits", []):
            if doc := hit.get("document"):
                link = f"/{document_type.lower()}s/{document_type.lower()}-{document_number}.html"
                docs.append(
                    DocumentHit(
                        document_type=document_type,
                        document_number=document_number,
                        link=link,
                        title=doc["title"],
                        snippet=hit["highlights"][0]["snippet"],
                    )
                )

    # commits
    for hit in results["results"][1].get("hits", []):
        # breakpoint()
        if commit := hit.get("document"):
            link = f"/commits/commit-{commit['commit_id']}.html"
            commits.append(
                CommitHit(
                    commit_id=commit["commit_id"],
                    link=link,
                    title=commit["commit_id"],
                    snippet=hit["highlights"][0]["snippet"],
                )
            )

    return docs, commits
