#FROM node:18-alpine
FROM python:3.10-alpine3.18

RUN apk update && apk upgrade
RUN apk add --no-cache --virtual .build-deps \
    curl \
    ca-certificates gcc \
    postgresql-dev postgresql-client \
    linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev

WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .

RUN pip3 install pipenv

# installs all packages from Pipfile.lock
#RUN pipenv sync
RUN pipenv install --deploy --ignore-pipfile

COPY . .

# run server in virtual environment with
#RUN pipenv shell
RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/get_public_ip.sh

EXPOSE 3000

ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD [ "pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:3000" ]
