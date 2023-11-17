#!/bin/sh

while ! pg_isready -d djangodb -h '192.130.0.2' -p 5432 -U postgres; do
#while ! psql -d djangodb -h '192.130.0.2' -p 5432 -U postgres < $DB_PASS; do
    echo "Waiting for postgres connection ..." >> db_conn.log
    sleep 1
done
echo 'SUCCESSFULLY CONNECTED TO POSTGRES FROM DJANGO !!' >> db_conn.log

while ! redis-cli -h $REDIS_HOST -a $REDIS_PW ping; do
#while ! psql -d djangodb -h '192.130.0.2' -p 5432 -U postgres < $DB_PASS; do
    echo "Waiting for redis connection ..." >> db_conn.log
    sleep 1
done
echo 'SUCCESSFULLY CONNECTED TO REDIS CACHE SERVER FROM DJANGO !!' >> db_conn.log
#curl -X GET -fsSL -m 1 'https://ident.me' > 'public.ip'

pipenv run python3 manage.py migrate
exec $@