#!/bin/sh

echo "PRESSING THE BIG MIGRATE BUTTON"
npx prisma migrate deploy
echo "RELEASING THE BIG MIGRATE BUTTON"

exec "$@"