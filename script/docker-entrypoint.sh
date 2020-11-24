#!/bin/sh
conffile="/etc/uwsgi/uwsgi.ini"

[ -z "${UWSGI_WORKERS_STEP}" ]       && UWSGI_WORKERS_STEP=1
[ -z "${WORKERS_IDLE_TIMEOUT}" ]     && WORKERS_IDLE_TIMEOUT=60
[ -z "${WORKERS_INITIAL}" ]          && WORKERS_INITIAL=4
[ -z "${WORKERS_MIN_IDLE}" ]         && WORKERS_MIN_IDLE=2
[ -z "${WORKERS_MAX}" ]              && WORKERS_MAX=6


cat <<EOF > "${conffile}"
[uwsgi]
socket = /tmp/uwsgi.sock
chown-socket = nginx:nginx
chmod-socket = 664
cheaper-algo = spare2
cheaper-step = ${UWSGI_WORKERS_STEP}
cheaper-idle = ${WORKERS_IDLE_TIMEOUT}
cheaper-initial = ${WORKERS_INITIAL}
cheaper = ${WORKERS_MIN_IDLE}
workers = ${WORKERS_MAX}
listen = $(sysctl -n net.core.somaxconn)
base = /var/www/html
home = /usr/local
vacuum = true
plugin = python3
module = wsgi:application
buffer-size = 65536
EOF

echo "Using the configuration file ${conffile}"
cat "${conffile}"
echo "====="
echo 

echo "Running entrypoint: $@"
exec "$@"