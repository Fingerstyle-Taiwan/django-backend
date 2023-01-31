FROM nginx:1.23.0-alpine

COPY ./nginx/* /etc/nginx/
COPY ./run.sh /run.sh

USER root

RUN apk add --no-cache openssl bash
RUN chmod +x /run.sh

VOLUME /vol/static
VOLUME /vol/www

CMD ["/run.sh"]