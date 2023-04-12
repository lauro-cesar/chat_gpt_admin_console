#!/bin/bash

set +x
# shellcheck disable=SC2034
# shellcheck disable=SC2155
export app_list=$(cat app_list.txt)
# shellcheck disable=SC2155
export backup_list=$(cat backup_list.txt)

# shellcheck disable=SC2034
# shellcheck disable=SC2155
export reset_migrations_list=$(cat reset_migrations_list.txt)

# shellcheck disable=SC2043
for app in $reset_migrations_list;
  do
    rm -rf $app/migrations/
    echo "removing migrations of $app"
  done



mkdir -p static/
mkdir -p media/
mkdir -p templates/


if [ ! -d ".venv" ]; then 
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ -z "${DATABASE_PORT}" ] ; then
    until nc -z "${DATABASE_HOST}" "${DATABASE_PORT}"; do
    echo "$(date) - waiting for database"
    sleep 5
done
fi

echo "Starting Redis Index"
python start_index.py 

echo "Starting Django"

# shellcheck disable=SC2043
for app in $app_list;
  do
    python manage.py makemigrations $app
  done

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput


# shellcheck disable=SC2043
for app in $backup_list;
  do
    if test -f "initial_data/$app.json"; then
        echo "Load backup for: $app"
        python manage.py loaddata initial_data/$app.json --skip-checks  --ignorenonexistent
    fi
  done



screen -wipe

# shellcheck disable=SC2086
screen -dmS queue celery -b redis://$REDIS_QUEUE_HOST:$REDIS_QUEUE_PORT -A project worker -B -E -Q $REDIS_QUEUE_QUEUE_NAME
echo "Global QUEUE started"

screen -dmS websocket daphne -b 0.0.0.0 -p 8002 --proxy-headers  project.asgi:application
echo "Global Async channels started"

screen -dmS django gunicorn project.wsgi:application --bind 0.0.0.0:8001 --proxy-protocol --strip-header-spaces --graceful-timeout=900 --timeout=900
echo "Django Started"

bash -c /home/chat_gpt_api/backup_apps.sh

export TERM=xterm
echo "Lets start TOP monitor tool"
screen -dmS monitor top
clear
while true
do
  sleep 28800
done
exec "$@"