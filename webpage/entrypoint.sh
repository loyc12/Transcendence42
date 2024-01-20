#!/bin/sh


while ! pg_isready -d djangodb -h '192.130.0.2' -p 5432 -U postgres; do
    echo "Waiting for postgres connection ..." >> db_conn.log
    sleep 1
done
echo 'SUCCESSFULLY CONNECTED TO POSTGRES FROM DJANGO !!' >> db_conn.log

while ! redis-cli -h $REDIS_HOST -a $REDIS_PW ping; do
    echo "Waiting for redis connection ..." >> db_conn.log
    sleep 1
done
echo 'SUCCESSFULLY CONNECTED TO REDIS CACHE SERVER FROM DJANGO !!' >> db_conn.log

pipenv run python3 manage.py makemigrations
pipenv run python3 manage.py migrate
pipenv run python3 manage.py collectstatic --noinput --clear

exec $@