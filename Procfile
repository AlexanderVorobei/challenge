worker: celery -A config.celery.app worker -l info
web: gunicorn config.wsgi:application --preload --timeout 15 --keep-alive 5