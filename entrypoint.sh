#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Run database migrations
echo "Applying database migrations..."
python healthpredict/manage.py migrate

# Collect static files (already done in build, but good safety)
# python healthpredict/manage.py collectstatic --noinput

# Create superuser if env vars are set
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser..."
    python healthpredict/manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email ${DJANGO_SUPERUSER_EMAIL:-admin@example.com} \
        || true
fi

# Exec the container's main process
exec "$@"
