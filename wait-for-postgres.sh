#!/bin/bash
# Skript zum Warten auf die Verfügbarkeit von PostgreSQL

set -e

host="$1"
shift
cmd="$@"

echo "Warten auf PostgreSQL bei $host..."

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "PostgreSQL ist nicht verfügbar - warte..."
  sleep 1
done

>&2 echo "PostgreSQL ist verfügbar - starte die Anwendung..."
exec $cmd