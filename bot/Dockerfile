FROM python:3.10-alpine

RUN apk add --no-cache libmagic

WORKDIR /home

COPY Pipfile.lock /home/
COPY Pipfile /home/

RUN pip install pipenv
RUN pipenv install --ignore-pipfile --skip-lock

COPY . /home/

EXPOSE 2005

CMD pipenv run python -m support_bot