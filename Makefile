
all:
	make up

up:
	docker-compose up --build -d

down:
	docker-compose down

local:
	cd webpage/ \
		&& pipenv install \
		&& pipenv run python manage.py runserver '0.0.0.0:3000'
