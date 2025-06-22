#!/bin/sh

if [ "$SERVICE_NAME" != "web" ]; then
    exec "$@"
    exit 0
fi

if [ -z "${DB_ENGINE}" ] || [ -z "${DB_HOST}" ] || [ -z "${DB_PORT}" ]; then
    echo "Need to set DB_ENGINE, DB_HOST, DB_PORT env variables to release containers"
    exit 1
fi

if [ "$DB_ENGINE" = "postgres" ]
then
    echo "PostgreSQL host: $DB_HOST port: $DB_PORT"
    echo "Waiting for postgres..."

    while ! nc -z "${DB_HOST}" "${DB_PORT}"; do
      echo "PostgreSQL is unavailable - sleeping"
      sleep 1
    done

    echo "**********************************"
    echo "*** PostgreSQL is up - started ***"
    echo "**********************************"
fi

if [ "$DB_REFRESH" = "True" ]
then
  echo "***********************************"
  echo "*** Refreshing de BD - starting ***"
  echo "***********************************"
  python manage.py flush --no-input
  python manage.py migrate
  python manage.py clearsessions
  python manage.py seeder
  python manage.py dummy
  python manage.py dummygiveaways
  python manage.py dummysales
  echo "************************************"
  echo "*** Refreshing de BD - completed ***"
  echo "************************************"
fi

if [ "$DEBUG" = "True" ]
then
  echo "**************************"
  echo "*** Execute fake sales ***"
  echo "**************************"
  python manage.py sell
fi

python manage.py collectstatic --no-input --clear

exec "$@"
