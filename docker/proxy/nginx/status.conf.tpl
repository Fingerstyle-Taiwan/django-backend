server {
    listen 8082;
    server_name  localhost;
    location /stub_status {
       stub_status on;
       allow localhost; #only allow requests from localhost
       deny all; #deny all other hosts 
       access_log off;
    }
}