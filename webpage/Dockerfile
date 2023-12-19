#FROM node:18-alpine
FROM python:3.10-alpine3.18

RUN apk update && apk upgrade
RUN apk add --no-cache --virtual .build-deps \
    curl \
    ca-certificates gcc \
    postgresql-dev postgresql-client \
    linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev \
    g++\
    redis\
    openssl\
    step-cli

WORKDIR /app

COPY Pipfile .

RUN pip install --upgrade pip
RUN pip3 install pipenv

# CERT + KEY +  self-signed SSL certificate
RUN openssl req -x509 -nodes -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=yourdomain.com"

# installs all packages from Pipfile.lock
RUN pipenv update
RUN pipenv install --deploy --ignore-pipfile

COPY . .

RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/djg_connect_to_postgres.sh

EXPOSE 3000

ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD [ "pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:3000"]

