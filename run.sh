#!/usr/bin/env sh
echo Run django migrations
python manage.py migrate || exit 0
echo Collect staticfiles
(python manage.py collectstatic --noinput --clear &&
touch staticfiles/.gitignore && echo "*/" >> staticfiles/.gitignore; exit 0)

exec "$@"

echo Creating django superuser
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (python manage.py createsuperuser --no-input; exit 0)
fi
echo Run server
python manage.py runserver 0.0.0.0:8000
