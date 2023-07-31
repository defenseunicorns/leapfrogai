#!/bin/bash

# Function to display script usage
function usage() {
    echo "Usage: $0 <CONNECTION_STRING>"
    exit 1
}

DATABASE="leapfrogai"

# Check if the first argument is provided
if [ -z "$1" ]; then
    echo "Error: PostgreSQL connection string not provided."
    usage
fi

# Assign the first argument to the CONNECTION_STRING variable
CONNECTION_STRING="$1"

# Check if psql command is available
if ! command -v psql &> /dev/null; then
    echo "Error: 'psql' command not found. Please make sure PostgreSQL is installed and in your system's PATH."
    exit 1
fi
echo "Found psql...attempting to connect to $USERNAME@$HOSTNAME."

# Connect to postgres and check if the leapfrogai database exists
# create if not exist
if [ "$( psql $CONNECTION_STRING -XtAc "SELECT 1 FROM pg_database WHERE datname='$DATABASE'" )" = '1' ]
then
    echo "Database already exists"
else
    echo "Database does not exist, creating"
    psql "$CONNECTION_STRING" -c "CREATE DATABASE $DATABASE;"
fi

# Check the exit status using $?
if [ $? -eq 0 ]; then
    echo "Database $DATABASE existence verified. You can now apply migrations to create tables."
else
    echo "Failed to connect to the provided postgres connection string and create database $DATABASE"
    exit 1
fi