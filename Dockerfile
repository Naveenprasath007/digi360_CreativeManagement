FROM ubuntu:20.04

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive


RUN apt-get update && apt-get install -y curl apt-transport-https python3 python3-pip python-dev locales
RUN apt-get install -y libpq-dev

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

#new command 

RUN apt-get install git

# here i need to modify**** my code 

COPY ./DigitalMarketing /app

WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]

