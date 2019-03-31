FROM python:3.7.3-alpine3.9

COPY Pipfile* /app/
WORKDIR /app

RUN apk add --no-cache gcc python3-dev postgresql-dev musl-dev \
    && pip install --no-cache-dir pipenv \
    && pipenv install --system

CMD ["python3"]
