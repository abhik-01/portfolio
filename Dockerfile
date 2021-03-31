FROM python:3.8.7
MAINTAINER abhikdas36@gmail.com

RUN apt-get update -y

COPY . /project

WORKDIR /project
RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT server:app