FROM python:3.10.7-alpine3.16
LABEL maintainer="linjianan1104@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG GOOGLE_CLIENT_ID=""
ARG GOOGLE_SECRET_KEY=""
ARG FACEBOOK_CLIENT_ID=""
ARG FACEBOOK_SECRET_KEY=""
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers  && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

ENV PATH="/py/bin:$PATH" \
    GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID \
    GOOGLE_SECRET_KEY=$GOOGLE_SECRET_KEY \
    FACEBOOK_CLIENT_ID=$FACEBOOK_CLIENT_ID \
    FACEBOOK_SECRET_KEY=$FACEBOOK_SECRET_KEY

USER django-user

