from golang:1.20.6 as migrate-runner

# install the postgresql client
RUN apt-get update && apt-get install -y \
  postgresql-client \
  && rm -rf /var/lib/apt/lists/*

# install the migrate script
RUN go install github.com/golang-migrate/migrate/v4/cmd/migrate@v4.16.2

WORKDIR /app

COPY create_db.sh .
COPY db_bootstrap.sh .

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