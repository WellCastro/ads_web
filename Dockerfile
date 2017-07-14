FROM ubuntu:latest
MAINTAINER Wellington Castro "wcesarc@gmail.com"

RUN apt-get update
RUN apt-get install -y python-pip

RUN mkdir -p /opt/deploy/ads_webpage
RUN mkdir -p /var/log/ads_webpage/webserver/
RUN mkdir -p /var/log/ads_webpage/application/

COPY . /opt/deploy/ads_webpage
RUN pip install -r /opt/deploy/ads_webpage/requirements.txt

WORKDIR /opt/deploy/ads_webpage

RUN python manage.py collectstatic --noinput

EXPOSE 8002
