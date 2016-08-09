#!/bin/bash

NPS_VERSION=1.11.33.2
NGINX_VERSION=1.10.1
TEMP_PATH=/var/local/lib/nginx
BUILD_DIR=/tmp/ngx

FLAGS=(
    --user=www-data
    --group=www-data
    --http-client-body-temp-path=$TEMP_PATH/body
    --http-fastcgi-temp-path=$TEMP_PATH/fastcgi
    --http-proxy-temp-path=$TEMP_PATH/proxy
    --http-scgi-temp-path=$TEMP_PATH/scgi
    --http-uwsgi-temp-path=$TEMP_PATH/uwsgi
    --with-http_ssl_module
    --add-module=$BUILD_DIR/ngx_pagespeed-release-${NPS_VERSION}-beta
)

mkpagespeed() {
    cd $BUILD_DIR
    wget https://github.com/pagespeed/ngx_pagespeed/archive/release-${NPS_VERSION}-beta.zip -O release-${NPS_VERSION}-beta.zip
    unzip release-${NPS_VERSION}-beta.zip
    cd ngx_pagespeed-release-${NPS_VERSION}-beta/
    wget https://dl.google.com/dl/page-speed/psol/${NPS_VERSION}.tar.gz
    tar -xzvf ${NPS_VERSION}.tar.gz  # extracts to psol/
}

mknginx() {
    cd $BUILD_DIR
    # check http://nginx.org/en/download.html for the latest version
    wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz
    tar -xvzf nginx-${NGINX_VERSION}.tar.gz
    cd nginx-${NGINX_VERSION}/
    ./configure ${FLAGS[@]}
    make
}

insnginx() {
 cd $BUILD_DIR/nginx-${NGINX_VERSION} && make install
}


while getopts :i opt; do
    case "$opt" in
         i) install=true ;;
        \?) echo "unknown option: $opt"; exit 1 ;;
    esac
done

shift $((OPTIND-1))

mkdir -p $TEMP_PATH
mkdir -p $BUILD_DIR
test -d $BUILD_DIR/ngx_pagespeed-release-${NPS_VERSION}-beta/psol || mkpagespeed
mknginx
$install && insnginx || exit 0
