# Database Migrations for Leapfrog

## Prerequisites

Install `migrate`

`go install github.com/golang-migrate/migrate/v4/cmd/migrate`

## Docker

In production, the following process will allow you to take a fresh PostgreSQL database and turn it into something that Leapfrog can use:

1. Run the `create_db.sh` command to create the leapfrogai database.
2. Run the migrations to create the necessary tables within the leapfrogai database.

```shell
docker run -v {{ migration dir }}:/migrations --network host migrate/migrate
    -path=/migrations/ -database postgres://localhost:5432/database up 2
```