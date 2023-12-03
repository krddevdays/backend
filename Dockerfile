FROM tiangolo/uwsgi-nginx:python3.9

ENV LISTEN_PORT 8080
EXPOSE 8080

WORKDIR /app

RUN pip install --no-cache-dir pipenv
COPY Pipfile* /app/
RUN pipenv install --system

COPY . .

RUN chmod +x /app/prestart.sh
