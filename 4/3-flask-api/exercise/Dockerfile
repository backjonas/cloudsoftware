FROM python:3.10.8-alpine3.16
WORKDIR /usr/app

RUN apk update
RUN apk add build-base libc-dev linux-headers zlib-dev jpeg-dev libjpeg

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]