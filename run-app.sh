#!/bin/bash

set -ex

if [ ! -z "$APP_EXEC_MODE_RUNSERVER" ]; then
    rm -rf static
    python manage.py collectstatic --noinput --settings=billy_project.settings.development
    python manage.py migrate --settings=billy_project.settings.development
    echo "Create Superuser"
    python manage.py createsu --settings=billy_project.settings.development --force-reset-password
    echo "Run App"
    exec python manage.py runserver --settings=billy_project.settings.development 0.0.0.0:8000
else
    python manage.py collectstatic --noinput --settings=billy_project.settings.production
    python manage.py migrate --settings=billy_project.settings.production
    python manage.py createsu --settings=billy_project.settings.production $DJANGO_CREATE_SU_OPTIONS
    exec python run_logged_gunicorn_app.py
fi
