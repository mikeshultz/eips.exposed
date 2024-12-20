from pathlib import Path
from shutil import copyfile

from django.core.management.base import BaseCommand  # , CommandError
from eips import EIPs


class Command(BaseCommand):
    help = "Copy assets from document repo to django static dir."

    def add_arguments(self, parser):
        parser.add_argument(
            "-d",
            "--dest",
            type=Path,
            required=True,
        )
        parser.add_argument(
            "-w",
            "--workdir",
            type=Path,
        )

    def handle(self, *args, **options):
        kwargs = {"freshness": None}
        if workdir := options.get("workdir"):
            kwargs["workdir"] = workdir

        eips = EIPs(**kwargs)
        eips.repo_fetch()

        print("options['dest']", options["dest"])

        for asset_path, asset_relative in eips.assets:
            destfile = options["dest"] / asset_relative
            destfile.parent.mkdir(parents=True, exist_ok=True)
            copyfile(asset_path, destfile)
            print(f"Copied {asset_relative}")
