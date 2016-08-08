server {
    listen 80;
    server_name alphageekcs.com www.alphageekcs.com secure.alphageekcs.com www.secure.alphageekcs.com remote.alphageekcs.com www.remote.alphageekcs.com;
    root /usr/share/nginx/letsencrypt;
    location ^~ /.well-known {
        allow all;
    }
}
