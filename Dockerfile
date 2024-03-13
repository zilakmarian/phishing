FROM python:3.11-alpine

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app/
RUN ["pip", "install", "poetry==1.8.2"]

COPY ./pyproject.toml ./poetry.lock ./
RUN ["poetry", "install", "--only=main", "--no-interaction"]

COPY ./app.py ./init_db.py ./
COPY ./modules ./modules

EXPOSE 5000
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "5000", "--factory", "app:create_app"]