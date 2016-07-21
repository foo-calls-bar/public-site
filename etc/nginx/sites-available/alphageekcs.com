upstream alphageekcs_com {
	include /etc/nginx/conf.d/alphageek_upstream;
}

server {
    listen 80;
    server_name alphageekcs.com www.alphageekcs.com secure.alphageekcs.com www.secure.alphageekcs.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name alphageekcs.com www.alphageekcs.com secure.alphageekcs.com www.secure.alphageekcs.com;
    ssl_certificate /etc/letsencrypt/live/alphageekcs.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/alphageekcs.com/privkey.pem;
    ssl_dhparam /etc/ssl/certs/dh2048.pem;

    include /etc/nginx/conf.d/ssl_params;
    include /etc/nginx/conf.d/well_known;
    include /etc/nginx/conf.d/zoho_verify;
    include /etc/nginx/conf.d/static_root;

    location / {
        include /etc/nginx/conf.d/proxy_params;
        proxy_pass http://alphageekcs_com;
    }
}

