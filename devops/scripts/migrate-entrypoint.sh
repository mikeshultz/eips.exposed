#!/bin/env bash

if [[ -z "$TYPESENSE_HOST" ]]; then
    TYPESENSE_HOST="localhost"
fi

if [[ -z "$TYPESENSE_PORT" ]]; then
    TYPESENSE_PORT="8108"
fi

if [[ -z "$TYPESENSE_API_KEY" ]]; then
    echo "TYPESENSE_API_KEY is required"
    exit 1
fi

uv run -- python manage.py migrate \
    && uv run -- python manage.py init-typesense \
        --api-key $TYPESENSE_API_KEY \
        --host $TYPESENSE_HOST \
        --port $TYPESENSE_PORT
