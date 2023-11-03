
DJANGO_DIR	= ./django_service
CERTS_DIR	= $(DJANGO_DIR)/.certs
CERT_CRT	= .certs/transcendence.crt
CERT_KEY	= .certs/transcendence.key

BREW_DIR	= /home/linuxbrew/.linuxbrew
BREW_EXE	= /home/linuxbrew/.linuxbrew/bin/brew

all:
	docker-compose up --build -d

down:
	docker-compose down

local:
	cd django_service/ \
		&& pipenv install \
		&& pipenv run python3 manage.py runserver '0.0.0.0:3000'

https:	$(CERT_CRT) $(CERT_KEY)
	cd django_service/ \
		&& echo "Installing django server dependencies ... in silence ..." \
		&& pipenv install \
		&& pipenv run python3 manage.py runserver_plus \
			--cert-file=$(CERT_CRT) --key-file=$(CERT_KEY) '0.0.0.0:3000'

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

$(BREW_EXE): _update_and_certutils
	@if [ ! -f $(BREW_EXE) ]; then \
		./ShellScripts/mkcert_install.sh $(BREW_DIR) $(BREW_EXE); \
	fi

$(CERT_CRT) $(CERT_KEY):	$(BREW_EXE)
	@if [ ! -f $(CERT_CRT) && ! -f $(CERT_KEY) ]; then \
		mkcert -install \
			&& cd django_service/ \
			&& mkcert -cert-file $(CERT_CRT) -key-file $(CERT_KEY) localhost 127.0.0.1; \
	fi
### <<<< DEPENDENCY INSTALLS END
