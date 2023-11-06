
DJANGO_DIR	= ./django_service
CERTS_DIR	= $(DJANGO_DIR)/.certs
LOCAL_CERT_CRT	= .certs/transcendence.crt
LOCAL_CERT_KEY	= .certs/transcendence.key
CERT_CRT	= $(DJANGO_DIR)/$(LOCAL_CERT_CRT)
CERT_KEY	= $(DJANGO_DIR)/$(LOCAL_CERT_KEY)

BREW_DIR	= /home/linuxbrew/.linuxbrew
BREW_EXE	= /home/linuxbrew/.linuxbrew/bin/brew

MKCERT_PATH	= /usr/bin/mkcert

all:	public_ip
	docker-compose up --build -d

down:
	docker-compose down

local:	public_ip
	cd django_service/ \
		&& pipenv install \
		&& pipenv run python3 manage.py runserver '0.0.0.0:3000'

https:	$(CERT_CRT) $(CERT_KEY)
	cd django_service/ \
		&& echo "Installing django server dependencies ... in silence ..." \
		&& pipenv install \
		&& pipenv run python3 manage.py runserver_plus \
			--cert-file=$(LOCAL_CERT_CRT) --key-file=$(LOCAL_CERT_KEY) '0.0.0.0:3000'


### DEPENDENCY INSTALLS START >>>
install: _install_python_pipenv	$(CERT_CRT)
	# ... Add dependency installation as needed.

_install_python_pipenv:
	@if [ ! $(which python;) ]; then \
		sudo apt-get install python3.10 -y \
			&& pip install pipenv; \
	fi

_update_and_certutils:
	sudo apt-get update -y && sudo apt-get upgrade -y
	sudo apt-get install	\
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

#	@if [ ! -f $(MKCERT_PATH) ]; then \
		./shellscripts/mkcert_install.sh $(MKCERT_PATH);\
	fi

$(BREW_EXE): _update_and_certutils
	@if [ ! test -f $(BREW_EXE) ]; then \
		./shellscripts/mkcert_install.sh $(BREW_DIR) $(BREW_EXE); \
	fi

$(CERT_CRT) $(CERT_KEY):	$(MKCERT_PATH)
	@if [ ! test -f $(CERT_CRT) || ! test -f $(CERT_KEY) ]; then \
		echo "INSIDE CERTS dependency if statment"\
			&& mkcert -install \
			&& mkcert -cert-file $(CERT_CRT) -key-file $(CERT_KEY) localhost 127.0.0.1; \
	fi
	test -f $(CERT_CRT) && test -f $(CERT_KEY)
### <<<< DEPENDENCY INSTALLS END
