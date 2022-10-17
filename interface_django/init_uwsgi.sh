#!/bin/bash
/usr/local/bin/uwsgi --ini /usr/local/operacao-autonoma/interface_django/interface_django_uwsgi.ini --emperor /etc/uwsgi/vassals --uid www-data --gid www-data --daemonize /var/log/uwsgi-emperor.log
