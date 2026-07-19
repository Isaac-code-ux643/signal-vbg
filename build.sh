#!/bin/bash
echo "Building Signal VBG..."
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py seed_centers
echo "Build complete!"
