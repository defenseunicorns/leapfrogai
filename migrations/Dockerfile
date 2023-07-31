from golang:1.20.6 as migrate-runner

# install the postgresql client
RUN apt-get update && apt-get install -y \
  postgresql-client \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# install the migrate script
RUN go mod init defenseunicorns.com/leapfrogai/migrate
RUN go get -u -d github.com/mattes/migrate/cli github.com/lib/pq
RUN go build -tags 'postgres' -o bin/migrate github.com/mattes/migrate/cli
# RUN go install github.com/golang-migrate/migrate/v4/cmd/migrate@v4.16.2

# Copy in scripts
COPY create_db.sh .
COPY db_bootstrap.sh .

# Copy in sql migration files
COPY *.sql .

# Create a non-root user 'nonroot'
RUN groupadd -g 1000 nonroot && useradd -u 1000 -g nonroot -ms /bin/bash nonroot

# Change the ownership of the application files to the 'nonroot'
RUN chown -R nonroot:nonroot /app
RUN chmod +x create_db.sh db_bootstrap.sh

# Set the user to 'nonroot'
USER nonroot

ENV HOSTNAME localhost
ENV USERNAME postgres
ENV PASSWORD ""
ENV PORT 5432

WORKDIR /app

# Run the application (replace 'myapp' with your binary name)
CMD ./db_bootstrap.sh -h $HOSTNAME -u $USERNAME -w $PASSWORD -p $PORT