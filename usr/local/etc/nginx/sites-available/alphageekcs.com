upstream alphageekcs_com {
	include conf.d/alphageek_upstream;
}

server {
    listen 80;
    server_name alphageekcs.com www.alphageekcs.com secure.alphageekcs.com www.secure.alphageekcs.com;
#   return 301 https://$host$request_uri;
    return 301 http://alphageek.xyz$request_uri;
}

server {
    listen 443 ssl;
    server_name alphageekcs.com www.alphageekcs.com secure.alphageekcs.com www.secure.alphageekcs.com;
    ssl_certificate /etc/letsencrypt/live/alphageekcs.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/alphageekcs.com/privkey.pem;
    ssl_dhparam /etc/ssl/certs/dh2048.pem;

    include conf.d/ssl_params;
    include conf.d/well_known;
    return 301 https://alphageek.xyz$request_uri;
    include conf.d/zoho_verify;
    include conf.d/static_root;

    location / {
        include conf.d/proxy_params;
        proxy_pass http://alphageekcs_com;
    }

}

