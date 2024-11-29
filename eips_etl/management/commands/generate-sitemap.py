from datetime import UTC, datetime

from django.core.management.base import BaseCommand  # , CommandError
from django.template.loader import render_to_string

from eips_etl.data import generate_sitemap, get_latest_commits
from eips_etl.models import Sitemap


class Command(BaseCommand):
    help = "Generate sitemap"

    def add_arguments(self, parser):
        parser.add_argument("-b", "--baseurl", type=str, default="https://eips.exposed")

    def handle(self, *args, **options):
        try:
            latest_commit = get_latest_commits(1)[0]
        except IndexError:
            print("ERROR: No commits found. Exiting...")
            return

        latest_gentime_res = Sitemap.objects.raw(
            "SELECT sitemap_id, generation_time FROM eips_etl_sitemap ORDER BY generation_time DESC LIMIT 1;"
        )
        latest_gentime = (
            latest_gentime_res[0].generation_time
            if latest_gentime_res
            else datetime.min.replace(tzinfo=UTC)
        )

        if latest_gentime >= latest_commit["commit_time"]:
            print("No new commits since last sitemap generation. Exiting...")
            return

        urls = list(generate_sitemap())
        sitemap_xml = render_to_string(
            "sitemap.xml",
            context=dict(base_url=options["baseurl"], urls=urls),
        )
        sitemap = Sitemap(xml_data=sitemap_xml)
        sitemap.save()

        print(f"Generated sitemap with {len(urls)} URIs (id: {sitemap.sitemap_id})")
