#!/bin/sh
echo "requirepass" $REDIS_PW >> /usr/local/etc/redis/redis.conf;
exec $@;