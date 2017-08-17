FROM ubuntu:16.04

MAINTAINER gimo <self@gimo.me> 

RUN apt-get clean && apt-get -y update && apt-get install -y locales && locale-gen en_US.UTF-8 && apt-get install python3-pip python3-dev -y && mkdir -p /deploy/app
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  

COPY gunicorn_config.py /deploy/gunicorn_config.py
COPY requirements.txt /deploy/requirements.txt
RUN pip3 install -r /deploy/requirements.txt

COPY service_account.json /deploy/service_account.json
COPY app /deploy/app


WORKDIR /deploy/app
EXPOSE 8000
ENV GOOGLE_APPLICATION_CREDENTIALS=/deploy/service_account.json
CMD ["/usr/local/bin/gunicorn", "--config", "/deploy/gunicorn_config.py", "app:app"]
