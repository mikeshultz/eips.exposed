#!/bin/env bash

uv run -- python manage.py update-ercs
uv run -- python manage.py update-eips
