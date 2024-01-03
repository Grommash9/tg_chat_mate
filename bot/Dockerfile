FROM python:3.10

WORKDIR /home

COPY Pipfile.lock /home/
COPY Pipfile /home/

RUN pip install pipenv
RUN pipenv install --ignore-pipfile

COPY . /home/

EXPOSE 2005

CMD pipenv run python -m support_bot