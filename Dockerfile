FROM python:3.7.4-alpine3.10
MAINTAINER sappy sappy5678@gmail.com


COPY ./ /app/
WORKDIR /app/

RUN ["/usr/local/bin/pip", "install", "-r", "requirements.txt"]

CMD ["python", "api.py"]
