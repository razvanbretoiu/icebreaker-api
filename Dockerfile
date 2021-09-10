FROM python:3.9

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY ./Pipfile ./
COPY ./Pipfile.lock ./

RUN pip install pipenv
RUN pipenv install --system

COPY . ./

EXPOSE $PORT

CMD exec gunicorn --bind :$PORT --workers 3 --threads 4 src.endpoints:app
