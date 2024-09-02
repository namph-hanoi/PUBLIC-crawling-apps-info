FROM python:3.10-slim-buster AS development

ARG APP_PORT
ENV GUNICORN_APP_PORT=${APP_PORT}

WORKDIR /app
COPY requirements.txt /app/
COPY scripts/install-chrome-driver.sh /app/scripts/install-chrome-driver.sh
RUN apt update && apt install unzip wget -y
RUN bash /app/scripts/install-chrome-driver.sh

RUN cd /app \
  && pip install -r requirements.txt --no-cache-dir

COPY . /app
# Extend the timeout to 30 minutes (1800)
CMD gunicorn -b 0.0.0.0:${GUNICORN_APP_PORT} app:app --timeout 1800