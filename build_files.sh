#!/bin/bash

# Use the correct Python version
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput


# python -m venv .venv
# source venv/Scripts/activate
# pip install -r requirements.txt 
# python manage.py collectstatic --noinput
