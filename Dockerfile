FROM python:3.7.3-alpine3.9

RUN apk add --no-cache gcc python3-dev postgresql-dev musl-dev

RUN pip install --no-cache-dir pipenv

COPY Pipfile* /app/
WORKDIR /app

RUN pipenv install --system

CMD ["python3"]
