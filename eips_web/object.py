from dataclasses import dataclass


@dataclass
class SitemapURL:
    loc: str
    lastmod: str
    changefreq: str | None = None
    priority: str | None = None
