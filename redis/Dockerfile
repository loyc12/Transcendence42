FROM redis:7.2-alpine3.18

COPY ./conf/redis_pw_inject.sh .
RUN chmod +x redis_pw_inject.sh
COPY ./conf/redis.conf /usr/local/etc/redis/redis.conf

ENTRYPOINT ["./redis_pw_inject.sh"]
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
