#!/bin/env bash

if [[ -z "$TYPESENSE_HOST" ]]; then
    TYPESENSE_HOST="localhost"
fi

if [[ -z "$TYPESENSE_PORT" ]]; then
    TYPESENSE_PORT="8108"
fi

uv run -- python manage.py migrate \
    && uv run -- python manage.py init-typesense \
        --api-key asdf1234 \
        --host $TYPESENSE_HOST \
        --port $TYPESENSE_PORT
