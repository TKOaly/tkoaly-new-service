#!/bin/bash
echo "===== Startup ====="
python manage.py runserver 0.0.0.0:${PORT:-8000}