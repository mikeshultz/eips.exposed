#!/bin/env bash

uv run -- python manage.py update-ercs
uv run -- python manage.py update-eips
uv run -- python manage.py generate-sitemap
