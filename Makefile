
DJANGO_DIR	= ./webpage
CERTS_DIR	= $(DJANGO_DIR)/.certs
LOCAL_CERT_CRT	= .certs/transcendence.crt
LOCAL_CERT_KEY	= .certs/transcendence.key
CERT_CRT	= $(DJANGO_DIR)/$(LOCAL_CERT_CRT)
CERT_KEY	= $(DJANGO_DIR)/$(LOCAL_CERT_KEY)

BREW_DIR	= /home/linuxbrew/.linuxbrew
BREW_EXE	= /home/linuxbrew/.linuxbrew/bin/brew

MKCERT_PATH	= /usr/bin/mkcert

DOTENV		= .env

RED			= '\033[1;91m'
DEFCOL		= '\033[0m'


all:	_activate_db_mode $(DOTENV)
	@if [ ! -d ./postgres/volume/data ]; then\
		mkdir -p ./postgres/volume/data;\
	fi
	docker-compose up --build -d

down:
	docker-compose down



local:	_deactivate_db_mode $(DOTENV)
	cd webpage/ \
		&& pipenv install \
		&& pipenv run python3 manage.py runserver '0.0.0.0:3000'

https:	_deactivate_db_mode $(DOTENV) $(CERT_CRT) $(CERT_KEY)
	cd webpage/ \
		&& echo "Installing django server dependencies ... in silence ..." \
		&& pipenv install \
		&& pipenv run python3 manage.py runserver_plus \
			--cert-file=$(LOCAL_CERT_CRT) --key-file=$(LOCAL_CERT_KEY) '0.0.0.0:3000'

re: down all

logs:
	docker logs $(shell docker ps -aqf "name=^django_backend")

connect:
	docker exec -it $(shell docker ps -aqf "name=^django_backend") /bin/sh

db_connect:
	docker exec -it $(shell docker ps -aqf "name=^django_backend") /bin/sh /app/djg_connect_to_postgres.sh
	

_activate_db_mode:		$(DOTENV)
	@sed -i 's/DJG_WITH_DB=\"\"/DJG_WITH_DB=True/g' .env
_deactivate_db_mode:	$(DOTENV)
	@sed -i 's/DJG_WITH_DB=True/DJG_WITH_DB=\"\"/g' .env


### DEPENDENCY INSTALLS START >>>
install: _install_python_pipenv	$(CERT_CRT)
	# ... Add dependency installation as needed.

$(DOTENV):
	# Tests that .env exist and is not empty
	@if [ ! -s .env ]; then\
		echo $(RED) "MISSING OR EMPTY .env FILE" $(DEFCOL);\
		exit 1;\
	fi


_install_python_pipenv:
	@if [ ! $(which python;) ]; then \
		sudo apt-get install python3.10 -y \
			&& pip install pipenv; \
	fi

_update_and_certutils:
	sudo apt-get update -y && sudo apt-get upgrade -y
	sudo apt-get install -y	\
		libpq-dev \
		libnss3-tools

$(MKCERT_PATH): _update_and_certutils

	@echo "MKCERT_PATH dependency"
	@if [ ! -f $(MKCERT_PATH) ]; then \
			echo "INSIDE MKCERT_PATH dependency if statment"\
			&& wget "https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-amd64"\
			&& sudo mv "mkcert-v1.4.3-linux-amd64" $(MKCERT_PATH)\
			&& sudo chmod +x $(MKCERT_PATH)\
			&& mkcert --version;\
	fi

$(BREW_EXE): _update_and_certutils
	@if [ ! test -f $(BREW_EXE) ]; then \
		./shellscripts/mkcert_install.sh $(BREW_DIR) $(BREW_EXE); \
	fi

$(CERT_CRT) $(CERT_KEY):	$(MKCERT_PATH)
	@if [ ! test -f $(CERT_CRT) || ! test -f $(CERT_KEY) ]; then \
		echo "INSIDE CERTS dependency if statment"\
			&& mkdir $(CERTS_DIR)\
			&& mkcert -install \
			&& mkcert -cert-file $(CERT_CRT) -key-file $(CERT_KEY) localhost 127.0.0.1; \
	fi
	test -f $(CERT_CRT) && test -f $(CERT_KEY)
### <<<< DEPENDENCY INSTALLS END
