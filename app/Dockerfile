# Pull base image
FROM python:3.9

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /code/app
WORKDIR /code/app

# Install dependencies
RUN pip install pipenv
#COPY Pipfile /code/
#COPY Pipfile.lock /code/
RUN pipenv install --system --dev

WORKDIR /code

#COPY . /code/app

EXPOSE 3030

# set in docker-compose.yml
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
