FROM debian:6

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y \
        gcc \
        python-configobj \
        python-dev \
        python-pip \
        python-setuptools \
        sudo && \
    apt-get autoclean

