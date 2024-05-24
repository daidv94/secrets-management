FROM 340396142553.dkr.ecr.ap-southeast-1.amazonaws.com/python:3.9-slim-buster-eyaml-gpg

WORKDIR /usr/app

COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

COPY ./src/ ./
