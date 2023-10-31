
DJANGO_DIR	= ./django_service
CERTS_DIR	= $(DJANGO_DIR)/.certs
#CERT_CRT	= $(CERTS_DIR)/transcendence.crt
#CERT_KEY	= $(CERTS_DIR)/transcendence.key
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
		&& pipenv run python manage.py runserver '0.0.0.0:3000'

https:	$(CERT_CRT) $(CERT_KEY)
	cd django_service/ \
		&& pipenv install \
		&& pipenv run python manage.py runserver_plus \
			--cert-file=$(CERT_CRT) --key-file=$(CERT_KEY) '0.0.0.0:3000'
#		&& pipenv run python manage.py runserver '0.0.0.0:3000'

_update_and_certutils:
	#sudo apt-get update -y && sudo apt-get upgrade -y
	#sudo apt-get install	\
	#	libnss3-tools

$(BREW_EXE): _update_and_certutils
	@if [ ! -f $(BREW_EXE) ]; then \
		./ShellScripts/mkcert_install.sh $(BREW_DIR) $(BREW_EXE); \
	fi
#	/bin/bash -c "$(shell curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" \
#		&& test -d ~/.linuxbrew && eval "$(shell ~/.linuxbrew/bin/brew shellenv)" \
#		&& test -d $(BREW_DIR) && eval "$(shell $(BREW_EXE) shellenv)" \
#		&& echo "eval \"\$(shell $(brew --prefix)/bin/brew shellenv)\"" >> ~/.bashrc \
#		&& brew install mkcert

$(CERT_CRT) $(CERT_KEY):	$(BREW_EXE)
	@if [ ! -f $(CERT_CRT) && ! -f $(CERT_KEY) ]; then \
		mkcert -install \
			&& cd django_service/ \
			&& mkcert -cert-file $(CERT_CRT) -key-file $(CERT_KEY) localhost 127.0.0.1; \
	fi

install:	$(CERT_CRT)
	# ... Add dependency installation as needed.