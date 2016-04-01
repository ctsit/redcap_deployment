#!/bin/bash
set -e

export MYTARGETDIR=$1

# determine the directory where this script resides
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# copy files to the correct target locations
mkdir -p $MYTARGETDIR
cp $DIR/index.php $MYTARGETDIR
cp $DIR/common.php $MYTARGETDIR
cp $DIR/det.php $MYTARGETDIR

# Make the required log directory and give the web server write access
mkdir -p /var/log/redcap
chown -R www-data.www-data /var/log/redcap

# Activate log rotation to assure we never have to worry about these logs
cat << EOF > /etc/logrotate.d/redcap-autonotify
/var/log/redcap/autonotify*.log {
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
