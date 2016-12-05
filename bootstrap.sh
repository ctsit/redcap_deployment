#!/bin/bash

# Contributors:
#    Christopher P. Barnes <senrabc@gmail.com>
#    Andrei Sura: github.com/indera
#    Mohan Das Katragadda <mohan.das142@gmail.com>
#    Philip Chase <philipbchase@gmail.com>
#    Ruchi Vivek Desai <ruchivdesai@gmail.com>
#    Taeber Rapczak <taeber@ufl.edu>
#    Josh Hanna <josh@hanna.io>

# Copyright (c) 2015, University of Florida
# All rights reserved.
#
# Distributed under the BSD 3-Clause License
# For full text of the BSD 3-Clause License see http://opensource.org/licenses/BSD-3-Clause

export DEBIAN_FRONTEND=noninteractive

# Exit on first error
set -e

echo "Import environment variables from /vagrant/.env"
. /vagrant/.env

# Indicate where the vagrant folder is mounted in the guest file system
SHARED_FOLDER=/vagrant

# Use the latest redcap*.zip file in $SHARED_FOLDER
REDCAP_ZIP=`ls $SHARED_FOLDER/redcap*.zip | grep "redcap[0-9]\{1,2\}\.[0-9]\{1,2\}\.[0-9]\{1,2\}\.zip" | sort -n | tail -n 1`

# import helper functions
. $SHARED_FOLDER/bootstrap_functions.sh
. $SHARED_FOLDER/redcap_deployment_functions.sh

# Pick a fast mirror...or at least one that works
log "Picking a fast mirror in the US..."
apt-get install -y netselect-apt
cd /etc/apt/
netselect-apt -c US > ~/netselect-apt.log 2>&1

# Update our repos
log "Updating apt package indicies..."
apt-get update

# Install developer tools
log "Execute: install_utils..."
install_utils

log "Execute: install_prereqs..."
install_prereqs $MYSQL_REPO $DB_ROOT_PASS
apt-get install -y php-pear php5-curl

# prep the /var/www directory
log "Prep the /var/www file system"
rm -rf /var/www/redcap/*

# extract a standard REDCap zip file as downloaded from Vanderbilt.
unzip -o -q $REDCAP_ZIP -d /var/www/

# adjust ownership so apache can write to the temp folders
chown -R www-data.root $PATH_TO_APP_IN_GUEST_FILESYSTEM/edocs/
chown -R www-data.root $PATH_TO_APP_IN_GUEST_FILESYSTEM/temp/

REDCAP_VERSION_DETECTED=`ls $PATH_TO_APP_IN_GUEST_FILESYSTEM | grep redcap_v | cut -d 'v' -f2 | sort -n | tail -n 1`
log "$REDCAP_ZIP content indicates REDCap version: $REDCAP_VERSION_DETECTED"

# create the empty databases and update the cake configuration
create_database $DB $DB_APP_USER $DB_APP_PASSWORD $DB_HOST $DB_ROOT_PASS

# Configure REDCap to use this database
update_redcap_connection_settings $PATH_TO_APP_IN_GUEST_FILESYSTEM $DB $DB_APP_USER $DB_APP_PASSWORD $DB_HOST $SALT

# make a config file for the mysql clients
write_dot_mysql_dot_cnf $DB $DB_APP_USER $DB_APP_PASSWORD $DB_ROOT_PASS

create_redcap_tables $DB $DB_APP_USER $DB_APP_PASSWORD $PATH_TO_APP_IN_GUEST_FILESYSTEM $REDCAP_VERSION_DETECTED

configure_redcap
configure_php_for_redcap
configure_redcap_cron
move_edocs_folder
set_hook_functions_file
make_twilio_features_visible
configure_exim4
check_redcap_status

# deploy extensions with developer settings

export PATH_TO_APP_IN_GUEST_FILESYSTEM

/vagrant/deploy_hooks.sh
/vagrant/deploy_plugins.sh
