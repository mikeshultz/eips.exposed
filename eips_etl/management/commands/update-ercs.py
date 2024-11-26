from pathlib import Path

from django.core.management.base import BaseCommand  # , CommandError
from eips import ERCs

from eips_etl.importer import import_repo


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

        count = import_repo(ERCs, **kwargs)
        print(f"Imported {count} ERCs")
