[![Run Status](https://api.shippable.com/projects/5ca0ddd5d964990007a0f147/badge?branch=master)]()
[![Coverage Badge](https://api.shippable.com/projects/5ca0ddd5d964990007a0f147/coverageBadge?branch=master)]()

# Installation

Copy `.env.example` to `.env` and fill variables

## Manual

1. Create database:
    ```sql
    # create user krddevdays with password 'krddevdays';
    # create database krddevdays owner krddevdays;
    ```
1. Initial virtualenv: 
    ```bash
    $ pipenv --python 3.7
    $ pipenv sync
    ```
1. Migrate database:
    ```bash
    $ ./manage.py migrate
    $ ./manage.py createsuperuser
    ```

## via docker-compose:

1. Build:
    ```bash
    $ docker-compose build
    ```
1. Start:
    ```bash
    $ docker-compose up postgres
    $ docker-compose up app
    ```
1. Run management command like:
    ```bash
    $ docker exec -it backend_app_1 /bin/sh
    /app # ./manage.py createsuperuser
    ```

# Test

```bash
# pipenv install --dev
# ./manage.py test --keepdb
```