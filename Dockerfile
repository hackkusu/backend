FROM python:3.8.10

ENV PYTHONUNBUFFERED 1

ARG REQUIREMENTS_FILENAME=base

RUN apt-get update && apt-get install -y \
  gettext \
  libpq-dev

COPY ./src/requirements /requirements

RUN pip install --upgrade pip && pip install -r /requirements/${REQUIREMENTS_FILENAME}.txt

WORKDIR /code
COPY ./src/ /code/

RUN python manage.py collectstatic
#COPY ./static/ /code/

#COPY ./ring-api.ini/ /code/polls/
# COPY ./ring-api.ini/ /code/
#COPY ./test_token.cache/ /code/polls/
# COPY ./test_token.cache/ /code/
#COPY ./gmail.credentials/ /code/polls/
#COPY ./gmail.credentials/ /code/

EXPOSE 7788
