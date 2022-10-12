FROM alpine:3.12
WORKDIR /usr/app

ENV VAR=10
ENV MSG="Hello Docker!"

COPY fibonacci.sh /usr/app
COPY helloDocker.sh /usr/app

RUN chmod +x /usr/app/fibonacci.sh
RUN chmod +x /usr/app/helloDocker.sh

CMD ["./fibonacci.sh"]
