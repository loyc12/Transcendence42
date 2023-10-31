
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
            models.py #CLASSES, DATA_STRUCT
            urls.py #LINK PATH
            views.py #EXECUTION

            apps.py  #TAGS
            admin.py #PV
            tests.py #PV
            auth/__init__.py # - - - - - - - - - - - - - - - - - - AUTH_USER
                models.py  #CLASSES, DATA_STRUCT
                urls.py
                views.py #EXECUTION

                apps.py #TAGS
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
                models.py  #CLASSES, DATA_STRUCT
                urls.py
                views.py #EXECUTION

                apps.py #TAGS
                admin.py #PV
                tests.py #PV
                templates/__init__.py # - - - - - - - - - - - - - -  PAGES
                            home/ # - - - - - - - - - - - - - - - - - HOME
                                css/empty.css
                                js/
                                    home.js
                                    select.js
                                home.html
                                init.html
                                select.html
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
    