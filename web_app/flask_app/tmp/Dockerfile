FROM ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    apt-utils \
    perl \
    wget \
    python3.9 \
    python3-pip \
    python3.9-dev \
    libffi-dev \
    gcc \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src \
 && wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz \
 && tar -zxvf install-tl-unx.tar.gz -C /usr/src

#WORKDIR /usr/src/install-tl-2022*

RUN cd /usr/src/install-tl-2022* \
 && echo I | ./install-tl -no-gui -repository http://mirror.ctan.org/systems/texlive/tlnet/

RUN /usr/local/texlive/202*/bin/x86_64-linux/tlmgr path add

#WORKDIR /root/result

COPY . /app
WORKDIR /app
#ENV FLASK_APP=app

#RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev bash

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#ENTRYPOINT ["python"]
#CMD ["rest.py"]
