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
    redis
#    sdl2-dev freetype-dev libpq-dev

# RUN apk add --no-cache --virtual .build-deps \
#     sdl2-dev freetype-dev

# RUN apk add --no-cache --virtual .build-deps \
#     libpq-dev

#RUN apk add libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev libportmidi-dev libjpeg-dev python3-setuptools python3-dev python3-numpy
WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install --upgrade pip
RUN pip3 install pipenv

#COPY requirements.txt .
#RUN pip3 install -r requirements.txt

# installs all packages from Pipfile.lock
RUN pipenv sync
RUN pipenv install --deploy --ignore-pipfile

COPY . .

RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/djg_connect_to_postgres.sh

EXPOSE 3000

ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD [ "pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:3000"]
