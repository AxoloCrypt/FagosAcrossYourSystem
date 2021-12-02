FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev libsdl2-dev libsdl2-image-dev gifsicle\
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 --no-cache-dir install --upgrade pip \
  && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["python3"]

RUN pip3 install --upgrade pip
RUN pip3 install -U pyxel
RUN pip3 install -U pyinstaller

WORKDIR /tmp/fagos

ADD main.py /tmp/fagos/
ADD assets/ /tmp/fagos/assets/
ADD images-fagos/ /tmp/fagos/images-fagos/

RUN pyxelpackager main.py
