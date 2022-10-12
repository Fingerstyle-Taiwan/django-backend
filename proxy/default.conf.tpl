server {
    listen ${LISTEN_PORT};
    listen [::]:${LISTEN_PORT};
    server_name api.fingerstyletaiwan.com;

    location /static {
        alias /vol/static;
    }

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$request_uri;
    }

}

server {
    listen 443 default_server ssl http2;
    listen [::]:443 ssl http2;

    server_name api.fingerstyletaiwan.com;

    ssl_certificate /etc/nginx/ssl/live/example.org/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/live/example.org/privkey.pem;

    location / {
        uwsgi_pass           ${APP_HOST}:${APP_PORT};
        include              /etc/nginx/uwsgi_params;
        client_max_body_size 10M;
    }
}