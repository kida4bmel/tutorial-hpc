FROM ubuntu:22.04

WORKDIR /hpc-util

ARG MYPORTARG=1234

ENV MYPORT=${MYPORTARG}

COPY requirements.txt /hpc-util/requirements.txt
COPY test.py /hpc-util/test.py

RUN apt update && apt install -y python3 python3-pip cmake

RUN pip install -r /hpc-util/requirements.txt

EXPOSE ${MYPORTARG}

ENTRYPOINT python3 -m http.server ${MYPORT}
