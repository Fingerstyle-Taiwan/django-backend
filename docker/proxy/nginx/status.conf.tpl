server {
    listen 8082;
    server_name  localhost;
    location /stub_status {
       stub_status on;
       access_log off;
    }
}