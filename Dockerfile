FROM tiangolo/uwsgi-nginx-flask:python3.7

MAINTAINER Ali Heyderli
RUN pip install pipenv
COPY . /app
WORKDIR /app
RUN pipenv install
EXPOSE 80
