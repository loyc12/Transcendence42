

all:
	docker-compose up --build -d

down:
	docker-compose down

local:
	cd django_service/ \
		&& pipenv install \
		&& pipenv run python manage.py runserver '0.0.0.0:3000'
