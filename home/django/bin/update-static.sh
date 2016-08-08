#!/bin/bash

. /usr/local/bin/virtualenvwrapper.sh &&
        workon agcs && cdproject && {
    ./manage.py generate_favicon --prefix 'assets/img/favicon/' agcs/static/img/agcs.png
    ./manage.py collectstatic --no-input && ./manage.py minify
}
