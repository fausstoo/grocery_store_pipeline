#!/bin/bash
set -e

if [ -z "$DB_ROOT_PASSWORD" ]; then
    echo >&2 'error: DB_ROOT_PASSWORD not set'
    exit 1
fi

if [ -z "$MYSQL_DATABASE" ]; then
    echo >&2 'error: MYSQL_DATABASE not set'
    exit 1
fi

# Set MySQL root password
echo "Setting up MySQL root password"
mysql --user=root <<MYSQL_SCRIPT
ALTER USER 'root'@'localhost' IDENTIFIED BY '$DB_ROOT_PASSWORD';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

# Run the default entrypoint
exec docker-entrypoint.sh "$@"
