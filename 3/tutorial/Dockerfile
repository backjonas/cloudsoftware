FROM alpine/socat
ARG LMAO=nou
ENV TEST2=$LMAO
EXPOSE 2000
ENTRYPOINT ["socat", "TCP4-LISTEN:2000,reuseaddr,fork", "EXEC:cat"]
