#!/bin/env bash

if [[ -z "$ASSETS_DIR" ]]; then
    echo "WARNING: ASSETS_DIR is not defined"
    export ASSETS_DIR=/tmp/assets
fi

#uv run -- python manage.py migrate
#uv run -- python manage.py init-typesense --api-key asdf1234
uv run -- python manage.py collectstatic --noinput
uv run -- python manage.py copy-assets -d $ASSETS_DIR

uv run -- python -m uvicorn eips_exposed.asgi:application \
    --host 0.0.0.0
