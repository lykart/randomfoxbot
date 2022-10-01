FROM python:3.8.14-slim-bullseye
RUN mkdir /app
WORKDIR /app
ADD . /app/

RUN apt-get update \ 
    && apt-get install -y libzbar0 libzbar-dev libpq-dev libjpeg-dev \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/ \
    && pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT python bot.py