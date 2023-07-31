# Database Migrations for Leapfrog

## Prerequisites

Install `migrate`

```shell
go get -u -d github.com/mattes/migrate/cli github.com/lib/pq
go build -tags 'postgres' -o bin/migrate github.com/mattes/migrate/cli
```

## Adding Migrations

```shell
migrate create -ext sql -dir /path/to/migrations -seq create_api_keys_table
```

So in our case:

```shell
./bin/migrate -path "migrations" -database "postgres://postgres:test@localhost:5432/leapfrogai?sslmode=disable" up
```

## Docker

In production, the following process will allow you to take a fresh PostgreSQL database and turn it into something that Leapfrog can use:

1. Run the `create_db.sh` command to create the leapfrogai database.
2. Run the migrations to create the necessary tables within the leapfrogai database.

```shell
docker run -v {{ migration dir }}:/migrations --network host migrate/migrate
    -path=/migrations/ -database postgres://localhost:5432/database up 2
```