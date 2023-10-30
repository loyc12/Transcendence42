
## Description

Ft-Transcendence

## Installation

```bash
source ./start.sh

```

## Running the app (without database)

```bash
make local 
```

## Test

## Arborescence
```bash
TRANSCENDENCE42/
    .env #PRIVATE
    .gitignore #PRIVATE
    docker-compose.yml
    Makefile
    Pipfile #DEPENDENCY
    Pipfile.lock #DEPENDENCY
    README.md
    start.sh #ENTRYPOINT UTILS
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -   
    django_service/
        Dockerfile
        entrypoint.sh #ACCESS DATA
        manage.py #PV DJANGO
        Pipfile #DEPENDENCY
        Pipfile.lock #DEPENDENCY
        api/__init__.py # - - - - - - - - - - - - - - - - - - - - - - - API
            apps.py
            models.py
            urls.py
            views.py

            admin.py #PV
            tests.py #PV
            auth/__init__.py # - - - - - - - - - - - - - - - - - - AUTH_USER
                apps.py
                models.py
                urls.py
                views.py

                admin.py #PV
                tests.py #PV
                migrations/__init__.py #DEPENDENCY
            migrations/__init__.py #DEPENDENCY
        core/__init__.py # - - - - - - - - - - - - - - - - - DJANGO_SERVICE
            asgi.py
            settings.py
            urls.py
            wsgi.py
        FrontApp/__init__.py # - - - - - - - - - - - - - - - - - FRONT_END
                apps.py
                models.py
                urls.py
                views.py
                
                admin.py #PV
                tests.py #PV
                dummy_responses/__init__.py # - - - - - - - - - - - - - 
                                dummy_responses.py
                templates/__init__.py # - - - - - - - - - - - - - - - -
                            hello.html
                            list_components.html
                migrations/__init__.py #DEPENDENCY
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -        
    postgres/
        Dockerfile
        volume/
    ShellScripts/
        .cmds.sh
        .colours.sh
        .gitquick.sh
        .help.sh
```


## Stay in touch


## License

### order command
    