from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path("search.html", views.search_html, name="search_html"),
    path("search.json", views.search_json, name="search_json"),
    path("eips/eip-<int:doc_id>.html", views.eip_html, name="eip_html"),
    path("eips/eip-<int:doc_id>.json", views.eip_json, name="eip_json"),
    path("ercs/erc-<int:doc_id>.html", views.erc_html, name="erc_html"),
    path("ercs/erc-<int:doc_id>.json", views.erc_json, name="erc_json"),
    path("ercs/<int:doc_id>", views.deprecated_erc_redirect, name="ercs_deprecated"),
    path("erc/<int:doc_id>", views.deprecated_erc_redirect, name="erc_deprecated"),
    path("eips/<int:doc_id>", views.deprecated_eip_redirect, name="eips_deprecated"),
    path("eip/<int:doc_id>", views.deprecated_eip_redirect, name="eip_deprecated"),
    path("commits/commit-<str:commit_id>.html", views.commit_html, name="commit_html"),
    path("commits/commit-<str:commit_id>.json", views.commit_json, name="commit_json"),
    path("parse-errors.html", views.parse_errors_html, name="parse_errors_html"),
    path("health.json", views.health_json, name="health_json"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap_xml"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path("index.html", views.index_html, name="index_html"),
    path("", views.index_html, name="index_html"),
]
