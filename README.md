# [eips.exposed](https://eips.exposed)

Ethereum EIP explorer

## Project Structure

### eips_exposed/processor/

This processes the official EIPs GitHub repository and inserts them into a PostgreSQL database.

### eips_exposed/server/

The Tornado server handling serving the GraphQL backend

### eips_frontend/

The source for the frontend application.

### ops/

Contains ops/devops scripts and data, including:

- Ansible scripts for deployment
- Dockerfiles for service containers
- Alembic migration files for DB management
- Configuration used in the docker containers
- Initial data, like tag defs and assignments
