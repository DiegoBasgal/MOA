#!/bin/bash
/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data --daemonize /var/log/uwsgi-emperor.log
