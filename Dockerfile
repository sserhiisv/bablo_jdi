FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk upgrade
RUN apk add --no-cache python3 python3-dev \
            linux-headers musl-dev uwsgi-python3 \
            uwsgi-http libevent-dev gcc

RUN apk add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

WORKDIR /web
ADD . /web

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install bash
RUN apk add --no-cache bash gawk sed grep bc coreutils

CMD python manage.py makemigrations
CMD python manage.py collectstatic --no-input
CMD python manage.py migrate
