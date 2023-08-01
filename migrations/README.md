# Database Migrations for Leapfrog

## Prerequisites

Build a local copy of the `migrate` cli

```shell
go get -u -d github.com/golang-migrate/migrate/v4/cli github.com/lib/pq
go build -v -tags 'postgres' -o bin/migrate github.com/golang-migrate/migrate/v4/cli
```

## Adding Migrations

```shell
migrate create -ext sql -dir /path/to/migrations -seq create_api_keys_table
```

So in our case (run from the leapfrogai root directory):

```shell
./bin/migrate create -ext sql -dir migrations -seq create_chat_table
```

Execute the migrations against your docker postgres running on localhost:

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

## Testing

Is the API key after hash and base64 encode reallllly the right length (88 characters)? What about trailing `==` signs in the base64?

`piVGcTaFcwWE7QJRPMX56RlG5BScibEYGpYNfT+/vX9e7MvH3Bi29xw9d6TE3TS5YfU78TCARTlRT5pbC75kyg==` is 88 characters, including the `==` sign.

Trying the following SQL statement in `psql` proves that postgres won't truncate in the background...it'll just straight up refuse to take your input if it's over 88 characters.

```sql
\c leapfrogai
insert into api_keys VALUES ('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'test');
ERROR:  value too long for type character varying(88)
```