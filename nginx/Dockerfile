FROM alpine:3.18.3

RUN apk update && apk upgrade && apk --no-cache add \
    nginx   \
    openssl

COPY ./conf/nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /run/nginx
RUN mkdir -p /ext
RUN mkdir -p /etc/nginx/ssl

RUN openssl req -x509 -noenc  \
        -out /etc/nginx/ssl/transcendence.crt       \
        -keyout /etc/nginx/ssl/transcendence.key    \
        -subj '/C=CN/ST=QC/L=Quebec/O=42/OU=transcendence/CN=transcendence.42.fr'

EXPOSE 443

ENTRYPOINT [ "nginx" , "-g", "daemon off;" ] 
# FROM nginx:latest
# FROM nginx:alpine

# RUN apk add --no-cache --virtual .build-deps \
#     curl \
#     ca-certificates \
#     openssl 

# # COPY ./conf/nginx.conf /etc/nginx/nginx.conf

# # # CA AUTH - - - - - - - - - - - - - - CA CERT + KEY + self-signed SSL certificate
#  RUN openssl genrsa -out ca.key
#  RUN openssl req -new -x509 -key ca.key -out ca.crt -days 365 -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=bazinga.com"

# # # # SERVER - - - - - - - - - - - - - - CA CERT + KEY + self-signed SSL certificate
#  RUN openssl genpkey -algorithm RSA -out transcendence.42.fr.key
#  RUN openssl req -new -key transcendence.42.fr.key -out transcendence.42.fr.csr -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=transcendence.42.fr"

# # # SIGN THE CSR WITH CA
# RUN openssl x509 -req -in transcendence.42.fr.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out transcendence.42.fr.crt -days 365

# EXPOSE 80
# EXPOSE 443

# COPY  ./conf/nginx.conf /etc/conf.d/nginx.conf

# # RUN  rm /etc/nginx/conf.d/default.conf
# # COPY nginx.conf /etc/nginx/nginx.conf
# ENTRYPOINT [ "nginx" , "-g", "daemon off;"]