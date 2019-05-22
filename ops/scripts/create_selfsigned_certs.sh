#!/bin/bash

mkdir -p /etc/letsencrypt/live/eips.exposed
mkdir -p /etc/letsencrypt/live/graphql.eips.exposed

openssl req -x509 -nodes -newkey rsa:1024 -days 1\
        -keyout "/etc/letsencrypt/live/eips.exposed/privkey.pem" \
        -out "/etc/letsencrypt/live/eips.exposed/cert.pem" \
        -subj "/CN=eips.exposed"

openssl req -x509 -nodes -newkey rsa:1024 -days 1\
        -keyout "/etc/letsencrypt/live/graphql.eips.exposed/privkey.pem" \
        -out "/etc/letsencrypt/live/graphql.eips.exposed/cert.pem" \
        -subj "/CN=graphql.eips.exposed"
