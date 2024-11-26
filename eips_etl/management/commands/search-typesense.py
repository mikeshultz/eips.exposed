from datetime import UTC, datetime
from typing import Any

import typesense
from django.core.management.base import BaseCommand  # , CommandError
from django.db import models
from django.forms.models import model_to_dict


def dump_dict(inst: type[models.Model], fields: list[str]) -> dict[str, Any]:
    def coerce(ov: Any) -> Any:
        if isinstance(ov, datetime):
            return int(ov.timestamp())  # unix timestamp
        return ov

    return {
        k: coerce(v)
        for k, v in model_to_dict(
            inst,
            fields=fields,
        ).items()
    }


class Command(BaseCommand):
    help = "Initialize a Typesense index"

    def add_arguments(self, parser):
        parser.add_argument("term", nargs="+", type=str)
        parser.add_argument("--host", type=str, default="localhost")
        parser.add_argument("--port", type=int, default=8108)
        parser.add_argument("--api-key", type=str)

    def _client(self, host: str, port: int, api_key: str):
        return typesense.Client(
            {
                "nodes": [{"host": host, "port": port, "protocol": "http"}],
                "api_key": api_key,
                "connection_timeout_seconds": 3,
            }
        )

    def handle(self, *args, **options):
        client = self._client(options["host"], options["port"], options["api_key"])
        result = client.collections["document"].documents.search(
            {
                "q": " ".join(options["term"]),
                "query_by": "title,description,commit,document_type,status,category,type,body",
                "sort_by": "updated:desc,created:desc",
                "group_by": "document_type,document_id",
                # "facet_by": "document_type,type",
            }
        )

        for group in result.get("grouped_hits", []):
            document_type = group["group_key"][0]
            document_id = group["group_key"][1]
            for hit in group.get("hits", []):
                doc = hit.get("document", {})
                print(
                    f"{document_type}-{document_id}: {doc['title']} ({datetime.fromtimestamp(doc['updated'], tz=UTC)})"
                )
                break  # only want the latest
