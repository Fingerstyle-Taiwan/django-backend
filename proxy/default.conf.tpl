server {
    listen ${LISTEN_PORT};
    listen [::]:${LISTEN_PORT};
    server_name fingerstyletaiwan.com www.fingerstyletaiwan.com;

    location /static {
        alias /vol/static;
    }

    location /api {
        uwsgi_pass           ${APP_HOST}:${APP_PORT};
        include              /etc/nginx/uwsgi_params;
        client_max_body_size 10M;
    }

    location / {
                proxy_pass http://localhost:3000;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
  }
}