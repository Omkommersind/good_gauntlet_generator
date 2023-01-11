FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN  apt-get -y update && apt-get -y install libsasl2-dev python-dev libldap2-dev libssl-dev

ADD . /code/
