# eips.exposed

A Django app that handles ETL and Web application for [eips.exposed](https://eips.exposed/).

## Development

### Database Setup

Create the postgres DB:

```psql
postgres=# create user eips;
CREATE ROLE
postgres=# create database eips;
CREATE DATABASE
postgres=# grant all on database eips to eips;
GRANT
postgres=# \connect eips
You are now connected to database "eips" as user "postgres".
postgres=# grant all on schema public to eips;
GRANT
```

Run the migrations:

```
$ python manage.py migrate
```

### TODO

Short term informal TODO.

- [X] Dockerfiles for services
- [X] Docker compose for local dev
- [X] Kubernetes helm charts and get ready for rollout
- [X] Mobile support
- [X] Add microdata for better sharing and search results
- [X] Add sitemap.xml
- [X] Get errors from python-eips and store in DB for reference and debugging
- [X] Link original documents, and format discussion link
- [ ] Handle deleted docs (e.g. ERC-1 leftover from EIP fork)
- [ ] Add browsing/directory page? By type/category? Need further categorization first?
- [ ] Figure out a way to intelligently understand what the author meant by `requires` (EIPs or ERCs)
- [ ] Show commit history on document page
- [ ] Serve documents by commit (`/eips/eip-20.html?commit=666deadbeef666`)
- [ ] Add search to header on all pages
- [ ] Finish up stats
- [ ] Finish up JSON endpoints
- [ ] Browser cache headers
- [ ] Look into ingress-nginx caching options
- [ ] Add document metrics (views, etc)
- [ ] Consider adding support for SIWE-authed comments
- [ ] Copy assets from repo to static file location and update references by django filter
- [ ] Consider serving assets per-commit, so older docs still have their version of their assets
