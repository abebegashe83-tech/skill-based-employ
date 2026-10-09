#!/usr/bin/env bash
set -o errexit

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-core.settings.production}"

python -m pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput