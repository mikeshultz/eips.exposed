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
