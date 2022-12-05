#!/bin/sh

echo "Waiting for database service..."

while ! nc -z "database" "5432"; do
  sleep 0.1
done

echo "Database service started."

if [ "$*" = "start_app_server" ]; then
  python source/manage.py migrate
  python source/manage.py collectstatic --no-input --clear
  gunicorn base.wsgi:application -c source/gunicorn.conf.py
elif [ "$*" = "start_celery_beat" ]; then
    celery --workdir source -A base beat -l INFO
elif [ "$*" = "start_celery_worker" ]; then
    celery --workdir source -A base worker -l INFO
else
  exec "$*"
fi
