#!/bin/sh

while ! pg_isready -d djangodb -h '192.130.0.2' -p 5432 -U postgres; do
#while ! psql -d djangodb -h '192.130.0.2' -p 5432 -U postgres < $DB_PASS; do
    echo "Waiting for postgres connection ..." >> db_conn.log
    sleep 1
done
echo 'SUCCESSFULLY CONNECTED TO POSTGRES FROM DJANGO !!' >> db_conn.log

exec $@