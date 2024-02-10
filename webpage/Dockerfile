#FROM node:18-alpine
FROM python:3.10-alpine3.18

RUN apk update && apk upgrade
RUN apk add --no-cache --virtual .build-deps \
    curl \
    gcc \
    postgresql-dev postgresql-client \
    linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev \
    g++\
    redis\
    py3-daphne

WORKDIR /app

COPY Pipfile .

RUN pip install --upgrade pip
RUN pip3 install pipenv

# installs all packages from Pipfile.lock
RUN pipenv update
RUN pipenv install --deploy --ignore-pipfile

COPY . .

RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/djg_connect_to_postgres.sh

EXPOSE 3000

ENTRYPOINT [ "/app/entrypoint.sh" ]
#CMD [ "pipenv", "run", "python", "manage.py", "runserver", "192.130.0.3:3000"]
CMD [ "pipenv", "run", "daphne", "-b", "192.130.0.3", "-p", "3000", "core.asgi:application" ]

