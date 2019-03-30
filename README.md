# Installation

## Manual

1. Create database:
    ```sql
    # create user krddevdays with password 'krddevdays';
    # create database krddevdays owner krddevdays;
    ```
2. Initial virtualenv: 
    ```bash
    $ pipenv --python 3.7
    $ pipenv sync
    ```
3. Migrate database:
    ```bash
    $ ./manage.py migrate
    $ ./manage.py createsuperuser
    ```

## via docker-compose:

1. Build:
    ```bash
    $ docker-compose up -d
    ```
2. Start/stop:
    ```bash
    $ docker-compose start
    $ docker-compose stop
    ```
3. Run management command like:
    ```bash
    $ docker exec -it backend_app_1 /bin/sh
    /app # ./manage.py createsuperuser
    ```
