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

# import helper functions
. $SHARED_FOLDER/bootstrap_functions.sh

# Pick a fast mirror...or at least one that works
log "Picking a fast mirror in the US..."
apt-get install -y netselect-apt
cd /etc/apt/
netselect-apt -c US > ~/netselect-apt.log 2>&1

# Setting oldstable debian repository
echo "deb http://debian.gtisc.gatech.edu/debian/ oldstable main contrib" > /etc/apt/sources.list
echo "deb-src http://debian.gtisc.gatech.edu/debian/ oldstable main contrib" >> /etc/apt/sources.list
echo "deb http://security.debian.org/ oldstable/updates main contrib" >> /etc/apt/sources.list
echo "deb-src http://security.debian.org/ oldstable/updates main contrib" >> /etc/apt/sources.list

# Update our repos
log "Updating apt package indicies..."
apt-get update

# Install developer tools
log "Execute: install_utils..."
install_utils

log "Execute: install_prereqs..."
install_prereqs $MYSQL_REPO $DB_ROOT_PASS

# prep the /var/www directory
log "Prep the /var/www file system"
if [ -d /var/www/redcap ]; then
    rm -rf /var/www/redcap
fi

if [ -L /var/www/redcap ]; then
    rm /var/www/redcap
fi

mkdir /var/www/redcap
cp /vagrant/files/prompt_to_install.html /var/www/redcap/index.html

# create the empty databases
create_database $DB $DB_APP_USER $DB_APP_PASSWORD $DB_HOST $DB_ROOT_PASS

# make a config file for the mysql clients
write_dot_mysql_dot_cnf $DB $DB_APP_USER $DB_APP_PASSWORD $DB_ROOT_PASS

# configure the mail server
configure_exim4

# install pdf toolkit
install_pdftk

# install composer
install_composer
