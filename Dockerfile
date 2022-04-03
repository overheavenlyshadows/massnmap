# This is a comment
FROM alpine:latest
RUN apk update
RUN apk add nmap masscan git wget python3 libpcap-dev
WORKDIR /app
RUN wget https://raw.githubusercontent.com/overheavenlyshadows/massnmap/master/massnmap.py -O massnmap.py
RUN chmod 777 massnmap.py
ENTRYPOINT ["python3", "massnmap.py"]