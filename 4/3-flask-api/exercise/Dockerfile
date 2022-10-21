FROM python:3.10.8-alpine3.16
WORKDIR /usr/app

RUN apk update
RUN apk add gcc libc-dev linux-headers zlib-dev jpeg-dev libjpeg

COPY requirements.txt /usr/app
RUN pip install -r requirements.txt

COPY app.py /usr/app/
COPY database /usr/app/database/

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]