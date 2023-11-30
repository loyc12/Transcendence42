
# DIR
DJANGO_DIR		= ./webpage
SHELLSCRIPTS 	= ./shellscripts

# SECRET
DOTENV			= .env
DOTCERT			= .certs/transcendence

# VERSION
VPYTHON			= python3.10
VCERT			= "mkcert-v1.4.3-linux-amd64"

# GET
GETCERT			= "https://github.com/FiloSottile/mkcert/releases/download/\
					v1.4.3/mkcert-v1.4.3-linux-amd64"\
# BIN CONTENT
BIN_PATH		= /usr/bin
BREW_PATH		= /home/linuxbrew/.linuxbrew
MKCERT_PATH		= $(BIN_PATH)/mkcert

# DATABASE CONTENT
DATA			= /postgres/volume/data

# NETWORK
PORT			= '0.0.0.0:3000'
LOCALHOST		= 127.0.0.1


# CERTIFICATE HANDLING
MKCERT 			= mkcert_install.sh
MKCERT_INST		= $(SHELLSCRIPTS)/$(MKCERT)

LOCAL_CERT_CRT	= $(DOTCERT).crt
LOCAL_CERT_KEY	= $(DOTCERT).key

CERTS_DIR		= $(DJANGO_DIR)/.certs
CERT_CRT		= $(DJANGO_DIR)/$(LOCAL_CERT_CRT)
CERT_KEY		= $(DJANGO_DIR)/$(LOCAL_CERT_KEY)

# BREW
BREW_EXE		= $(BREW_PATH)/bin/brew

GAME_SUBPATH	= $(DJANGO_DIR)/game/PingPongRebound
GAMEMANAGER		= $(GAME_SUBPATH)/GameManager.py

# COLOR
RED			= '\033[1;91m'
DEFCOL		= '\033[0m'

# DOCKER COMPOSE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
all:	_activate_db_mode $(DOTENV) $(GAME_SUBPATH)
	@if [ ! -d .$(DATA) ]; then\
		mkdir -p .$(DATA);\
	fi
	docker-compose up --build -d

down:
	docker-compose down

# LOCAL - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
local:	_deactivate_db_mode $(DOTENV)
	cd webpage/ \
		&& pipenv install \
		&& pipenv run python3 manage.py runserver $(PORT)

#	HTTPS_LOCAL
https:	_deactivate_db_mode $(DOTENV) $(CERT_CRT) $(CERT_KEY)
	cd webpage/ \
		&& echo "Installing django server dependencies ... in silence ..." \
		&& pipenv install \
		&& pipenv run python3 manage.py runserver_plus \
			--cert-file=$(LOCAL_CERT_CRT) --key-file=$(LOCAL_CERT_KEY) $(PORT)

re: down all

hard_re: down db_volume_reset all


#	Utility functions 
logs:
	docker logs $(shell docker ps -aqf "name=^django_backend")
db_logs:
	docker logs $(shell docker ps -aqf "name=^postgres_db")

connect:
	docker exec -it $(shell docker ps -aqf "name=^django_backend") /bin/sh
db_connect:
	docker exec -it $(shell docker ps -aqf "name=^django_backend") /bin/sh /app/djg_connect_to_postgres.sh

migrations:
	docker exec -it $(shell docker ps -aqf "name=^django_backend") pipenv run python manage.py makemigrations
migrate:
	docker exec -it $(shell docker ps -aqf "name=^django_backend") pipenv run python manage.py migrate

superuser:
	docker exec -it $(shell docker ps -aqf "name=^django_backend") pipenv run python manage.py createsuperuser

db_volume_reset:
	sudo rm -rf $(DATA)
	mkdir $(DATA) -p


### DEPENDENCY INSTALLS START >>>
install: _install_python_pipenv	$(CERT_CRT)

$(GAMEMANAGER):
	git submodule update --init --recursive

$(GAME_SUBPATH):	$(GAMEMANAGER)

#	python
_install_python_pipenv:
	@if [ ! $(which python;) ]; then \
		sudo apt-get install $(VPYTHON) -y \
		&& pip install pipenv; \
	fi

#	certs_utils
_update_and_certutils:
	sudo apt-get update -qq -y && sudo apt-get upgrade -qq -y
	sudo apt-get install -qq -y	\
		libpq-dev \
		libnss3-tools

$(MKCERT_PATH): _update_and_certutils
	@echo "MKCERT_PATH dependency"
	@if [ ! -f $(MKCERT_PATH) ]; then \
			echo "INSIDE MKCERT_PATH dependency if statment"\
			&& wget $(GETCERT)\
			&& sudo mv $(VCERT) $(MKCERT_PATH)\
			&& sudo chmod +x $(MKCERT_PATH)\
			&& mkcert --version;\
	fi

$(CERT_CRT) $(CERT_KEY):	$(MKCERT_PATH)
	@if [ ! test -f $(CERT_CRT) || ! test -f $(CERT_KEY) ]; then \
		echo "INSIDE CERTS dependency if statment"\
			&& mkdir $(CERTS_DIR)\
			&& mkcert -install \
			&& mkcert -cert-file $(CERT_CRT) -key-file $(CERT_KEY) localhost $(LOCALHOST); \
	fi
	test -f $(CERT_CRT) && test -f $(CERT_KEY)
### <<<< DEPENDENCY INSTALLS END

# MODE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
_activate_db_mode:		$(DOTENV)
	@sed -i 's/DJG_WITH_DB=\"\"/DJG_WITH_DB=True/g' $(DOTENV)
_deactivate_db_mode:	$(DOTENV)
	@sed -i 's/DJG_WITH_DB=True/DJG_WITH_DB=\"\"/g' $(DOTENV)

# _activate_db_mode:		$(DOTENV)
# 	@sed -i 's/DJG_WITH_DB=\"\"/DJG_WITH_DB=True/g' .env
# _deactivate_db_mode:	$(DOTENV)
# 	@sed -i 's/DJG_WITH_DB=True/DJG_WITH_DB=\"\"/g' .env

# SECURITY - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
#	.env
$(DOTENV):
	# Tests that .env exist and is not empty
	@if [ ! -s .env ]; then\
		echo $(RED) "MISSING OR EMPTY .env FILE" $(DEFCOL);\
		exit 1;\
	fi
