#!/bin/bash
# Function to display script usage
function usage() {
    echo "Usage: $0 -h <hostname> -u <username> -w <password> [-p <port>]"
    exit 1
}

# Initialize variables with default values
HOSTNAME="localhost"
USERNAME="postgres"
PASSWORD=""
PORT="5432"        # Default PostgreSQL port

# Parse command-line arguments using getopts
while getopts ":h:u:w:p:" opt; do
    case $opt in
        h)
            HOSTNAME="$OPTARG"
            ;;
        u)
            USERNAME="$OPTARG"
            ;;
        w)
            PASSWORD="$OPTARG"
            ;;
        p)
            PORT="$OPTARG"
            ;;
        \?)
            echo "Invalid option: -$OPTARG"
            usage
            ;;
        :)
            echo "Option -$OPTARG requires an argument."
            usage
            ;;
    esac
done

# Check if the mandatory arguments are provided
if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ]; then
    echo "Error: username and password are mandatory."
    usage
fi

# Check if psql command is available
if ! command -v psql &> /dev/null; then
    echo "Error: 'psql' command not found. Please make sure PostgreSQL is installed and in your system's PATH."
    exit 1
fi

# Construct the psql connection string
CONNECTION_STRING="postgresql://$USERNAME:$PASSWORD@$HOSTNAME:$PORT"

echo "Creating leapfrogai database"
./create_db.sh "$CONNECTION_STRING"
# Check the exit status using $?
if [ $? -ne 0 ]; then
    echo "Error: create_db.sh returned a non-zero exit status."
    exit 1
fi

echo "Running all migrations"
./bin/migrate -path "/app" -database "$CONNECTION_STRING/leapfrogai?sslmode=disable" up
# Check the exit status using $?
if [ $? -ne 0 ]; then
    echo "Error: migrate returned a non-zero exit status."
    exit 1
fi