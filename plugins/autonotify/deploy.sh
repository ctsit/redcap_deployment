#!/bin/sh
set -e

# Make the required log directory and give the web server write access
mkdir -p /var/log/redcap/autonotify
chown -R www-data.www-data /var/log/redcap

# Activate log rotation to assure we never have to worry about these logs
cat << EOF > /etc/logrotate.d/redcap-autonotify
/var/log/redcap/autonotify/*.log {
    weekly
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 640 www-data www-data
    sharedscripts
}
EOF
