FROM ubuntu:16.04

MAINTAINER gimo <self@gimo.me> 

RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  

RUN apt-get update -y
RUN apt-get install python3-pip python3-dev -y
RUN apt-get clean

RUN mkdir -p /deploy/app

COPY gunicorn_config.py /deploy/gunicorn_config.py
COPY requirements.txt /deploy/requirements.txt
COPY service_account.json /deploy/service_account.json
COPY app /deploy/app

RUN pip3 install -r /deploy/requirements.txt

WORKDIR /deploy/app
EXPOSE 8000
ENV GOOGLE_APPLICATION_CREDENTIALS=/deploy/service_account.json
CMD ["/usr/local/bin/gunicorn", "--config", "/deploy/gunicorn_config.py", "app:app"]
