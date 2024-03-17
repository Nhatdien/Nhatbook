FROM python:3.9-slim as base

WORKDIR /app

COPY pyproject.toml /app/
COPY poetry.lock /app/
# Install Poetry.\
RUN pip install poetry==1.4.2

COPY --chown=user:user ./pyproject.toml ./poetry.lock ./alembic.ini ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

FROM base as test

# Copy the rest of the application code
COPY . /app
EXPOSE 5000

# Command to run the FastAPI application
CMD ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
