# EIPs Exposed Ops

These are infrastructure and ops tools for deploying eips.exposed services.

## Services `.env` file

The `.env` file, created in the `eips_exposed_srcdir` must be created to properly configure the deployed services.  These are the required env vars:

- `EIPS_DB_URL` - The full URL for DB access
- `POSTGRES_USER`
- `POSTGRES_DB`
- `POSTGRES_PASSWORD`

### Example

    EIPS_DB_URL="postgresql://myuser:mypass@postgres/eips"
    POSTGRES_USER="myuser"
    POSTGRES_PASSWORD="mypass"
    POSTGRES_DB="eips"

## Deploy

    ansible-playbook ops/ansible/main.yam
