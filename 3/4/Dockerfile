FROM ubuntu:18.04
WORKDIR /application
ARG PYTHON_VERSION=3.8

RUN apt update
RUN echo $PYTHON_VERSION
RUN if [ "$PYTHON_VERSION" = "3.8" ]; then \
  apt install -y curl python3-distutils python3.8-dev \
  && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && python3.8 get-pip.py \
  && cp /usr/bin/python3.8 /usr/bin/python3; fi

RUN if [ "$PYTHON_VERSION" = "3.9" ]; then \
  apt install -y build-essential libssl-dev zlib1g-dev \
    libncurses5-dev libncursesw5-dev libreadline-dev \
    libsqlite3-dev libgdbm-dev libdb5.3-dev libbz2-dev \
    libexpat1-dev liblzma-dev libffi-dev uuid-dev curl \
  && curl -o python3_9.tar.gz https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz \
  && tar -xzf python3_9.tar.gz && rm python3_9.tar.gz \
  && cd Python-3.9.0 \
  && ./configure --with-ensurepip=install \
  && make -j 8 \
  && make install \
  && cp /usr/local/bin/python3.9 /usr/bin/python3 \
  && cp /usr/local/bin/pip3.9 /usr/bin/pip3; fi

RUN pip3 install wheel
RUN pip3 install -U pytest pylint nbmake