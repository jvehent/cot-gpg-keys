FROM python:3.5
MAINTAINER Aki Sasaki <aki@mozilla.com>

RUN apt-get update && apt-get install -y \
    gnupg2

RUN mkdir -p /work
RUN pyvenv /work
RUN /work/bin/pip install tox

WORKDIR /work
