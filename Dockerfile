FROM python:3.8.6-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/app

RUN cd /opt/app

WORKDIR /opt/app

COPY requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

COPY app ./opt/app/
COPY tests ./opt/tests
COPY entrypoint.sh /opt/entrypoint.sh

RUN chmod +x /opt/entrypoint.sh

VOLUME [ "/logs" ]

EXPOSE 5000

CMD "/bin/bash"