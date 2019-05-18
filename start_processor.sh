#!/bin/sh

# Run migrations
alembic upgrade head

# Start processor
python -m eips_exposed.processor -d
