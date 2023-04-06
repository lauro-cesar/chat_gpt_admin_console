#!/bin/bash


source variables.sh

echo "Setting up Python"
python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip &&  pip install -r $DOCKER_PROJECT_DIR/requirements.txt


echo "Make Migrations"
find $PROJECT_DIR/ -path "*/migrations/*.py" -not -name "__init__.py" -delete && find . -path "*/migrations/*.pyc"  -delete
cd $PROJECT_DIR/

python3 manage.py makemigrations accounts sites flatpages
python3 manage.py makemigrations
python3 manage.py migrate --noinput


if test -f "initial_data.json"; then
    python manage.py loaddata initial_data.json --ignorenonexistent
fi
python3 manage.py collectstatic --noinput
cd ..
