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
		guide.txt
   		start.sh #ENTRYPOINT UTILS
```


## Stay in touch

## License

### order command

<!--
- first: exode de script du html
- then:  set initState struct (each of them , but solo first...)
- console() init_status ... width, height, ratio,
- player.pos[x,y]:dir[0/1]...ball[bx,by],score[s1,s2],
-->

<!--
- new target: player's color on the lobby match game color
- paddle orientation : y // x
- setup *page and *button:  help!
    - menu button: "Help"
    - module 'page' to display game tuto!
- test de "bouton de nav" ...
    backward: to home (works!)
    forward: get back from last position
    refresh !?! ...
- crash at some point ... on endGame!!!
   -->