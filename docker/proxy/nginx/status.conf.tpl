server {
    listen 8082;
    server_name  localhost;
    location /stub_status {
       stub_status on;
       allow 127.0.0.1; #only allow requests from localhost
       deny all; #deny all other hosts 
       access_log off;
    }
}