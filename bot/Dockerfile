FROM python:3.10

WORKDIR /home

COPY . /home/

RUN pip install pipenv

RUN pipenv install --dev --ignore-pipfile

EXPOSE 2005

CMD pipenv run python -m support_bot