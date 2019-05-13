FROM tiangolo/uwsgi-nginx:python3.6-alpine3.9

RUN apk add --no-cache gcc python3-dev postgresql-dev musl-dev
RUN pip install --no-cache-dir pipenv

EXPOSE 8000

WORKDIR /app

COPY Pipfile* /app/
RUN pipenv install --system

COPY . .

RUN chmod +x /app/prestart.sh