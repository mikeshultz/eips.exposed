from pathlib import Path

from django.core.management.base import BaseCommand  # , CommandError
from eips import EIPs
from eips.const import ENCODING

from eips_etl.models import Commit, Document


class Command(BaseCommand):
    help = "Updates EIPs records in the dataase"

    def add_arguments(self, parser):
        parser.add_argument(
            "-w",
            "--workdir",
            type=Path,
        )

    def handle(self, *args, **options):
        print("args:", args)
        print("options:", options)
        kwargs = {"freshness": None}
        if workdir := options.get("workdir"):
            kwargs["workdir"] = workdir
        eips = EIPs(**kwargs)
        eips.repo_fetch()

        latest_commit = Commit.objects.all().order_by("-commit_time").first()
        count = 0
        for commit, doc in eips.all(
            until_commit=latest_commit.commit_id if latest_commit else None
        ):
            try:
                cobj = Commit.objects.get(commit_id=commit.id.decode(ENCODING))
                continue  # unnecessary to process documents if we already have the commit
            except Commit.DoesNotExist:
                cobj = Commit.from_dulwich(commit)
                cobj.save()

            try:
                dobj = Document.objects.get(document_id=doc.id, commit_id=commit)
            except Document.DoesNotExist:
                dobj = Document.from_dict(cobj, doc.model_dump())
                dobj.save()

            count += 1
