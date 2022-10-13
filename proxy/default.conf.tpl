server {
    listen ${LISTEN_PORT};
    server_name api.fingerstyletaiwan.com;

    location /static {
        alias /vol/static;
    }

    location / {
        uwsgi_pass           ${APP_HOST}:${APP_PORT};
        include              /etc/nginx/uwsgi_params;
        client_max_body_size 10M;
    }

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
}

