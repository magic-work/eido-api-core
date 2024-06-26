# Use Python 3.11.8 as the base image
FROM python:3.11.8

# Set the working directory in the container to /code
WORKDIR /code

# Copy the requirements file into the container
COPY ./pyproject.toml ./poetry.lock* /code/

# Install poetry
RUN pip install poetry

# Disable the creation of a virtual environment by poetry
RUN poetry config virtualenvs.create false

# Install the dependencies
RUN poetry install --no-dev

# Copy the rest of the application code into the container
COPY ./app /code/app

# Set the internal file paths in the app to the ones used by docker
ENV DOCKER_PATHS=true

# Set the internal file paths in the app to the ones used by docker
ENV ROOT_PATH=/eido

# Set the command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
