#!/bin/bash
/usr/local/bin/uwsgi --ini /opt/operacao-autonoma/moa_web/moa_web_uwsgi.ini --emperor /etc/uwsgi/vassals --uid www-data --gid www-data --daemonize /var/log/uwsgi-emperor.log
