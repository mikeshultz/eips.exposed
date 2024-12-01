from datetime import datetime
from typing import Any

import typesense
from django.core.management.base import BaseCommand  # , CommandError
from django.db import models
from django.forms.models import model_to_dict
from typesense.exceptions import ObjectNotFound

from eips_etl.models import Commit, Document, Person


def dump_dict(inst: type[models.Model], fields: list[str]) -> dict[str, Any]:
    def coerce(ov: Any) -> Any:
        if isinstance(ov, datetime):
            return int(ov.timestamp())  # unix timestamp
        if isinstance(ov, list):
            return ", ".join(str(ov))
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
        print("args:", args)
        print("options:", options)
        client = self._client(options["host"], options["port"], options["api_key"])

        try:
            client.collections["commit"].delete()
        except ObjectNotFound:
            pass
        try:
            client.collections["document"].delete()
        except ObjectNotFound:
            pass

        commit_schema = {
            "name": "commit",
            "fields": [
                {"name": "commit_id", "type": "string"},
                {"name": "author", "type": "string", "facet": True},
                {"name": "committer", "type": "string", "facet": True},
                {"name": "author_time", "type": "int64"},
                {"name": "commit_time", "type": "int64"},
                {"name": "message", "type": "string"},
            ],
            "default_sorting_field": "commit_time",
        }
        client.collections.create(commit_schema)

        document_schema = {
            "name": "document",
            "fields": [
                {"name": "document_number", "type": "int32", "facet": True},
                {"name": "document_number_string", "type": "string"},
                {"name": "commit", "type": "string", "facet": True},
                {"name": "document_type", "type": "string", "facet": True},
                {"name": "created", "type": "int64"},
                {"name": "updated", "type": "int64"},
                {"name": "status", "type": "string", "facet": True},
                {"name": "category", "type": "string", "facet": True},
                {"name": "type", "type": "string", "facet": True},
                {"name": "resolution", "type": "string"},
                {"name": "title", "type": "string"},
                {"name": "description", "type": "string"},
                {"name": "body", "type": "string"},
                {"name": "authors", "type": "string"},
            ],
            "default_sorting_field": "updated",
        }
        client.collections.create(document_schema)

        for commit in Commit.objects.all():
            doc = dump_dict(
                commit,
                fields=[
                    "commit_id",
                    "author",
                    "committer",
                    "author_time",
                    "commit_time",
                    "message",
                ],
            )
            author_id = doc["author"]
            committer_id = doc["committer"]
            doc["author"] = Person.objects.get(person_id=author_id).person_string
            doc["committer"] = Person.objects.get(person_id=committer_id).person_string

            client.collections["commit"].documents.create(doc)

        for document in Document.objects.all():
            doc = dump_dict(
                document,
                fields=[
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
                    "description",
                    "body",
                    "authors",
                ],
            )

            if not doc.get("created"):
                doc["created"] = 0
            if not doc.get("updated"):
                doc["updated"] = doc["created"]

            doc["document_number_string"] = (
                f"{doc['document_type']}-{doc['document_number']}"
            )

            client.collections["document"].documents.create(doc)
