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

export DATABASE_HOST=localhost
export DATABASE_NAME=redcap
export DATABASE_USER=redcap
export DATABASE_PASSWORD=password
export DATABASE_ROOT_PASS=123
export development_hostname=redcap.dev
export redcap_base_url=http://$development_hostname/redcap/
export smtp_smarthost=smtp.ufl.edu
export max_input_vars=10000
export upload_max_filesize=32M
export post_max_size=32M


function install_prereqs() {
    # Install the REDCap prerequisites:
    #   https://iwg.devguard.com/trac/redcap/wiki/3rdPartySoftware

    apt-get update

    apt-get install -y \
        apache2 \
        mysql-server \
        php5 php-pear php5-mysql php5-curl \
        php5-gd \
        unzip git php5-mcrypt

    # configure MySQL to start every time
    update-rc.d mysql defaults

    # restart apache
    service apache2 restart
}

# Setup REDCap
function install_redcap() {
    rm -rf /var/www/*

    # extract a standard REDCap zip file as downloaded from Vanderbilt.
    unzip -q $REDCAP_ZIP -d /var/www/

    # adjust ownership so apache can write to the temp folders
    chown -R www-data.root /var/www/redcap/edocs/
    chown -R www-data.root /var/www/redcap/temp/

    REDCAP_VERSION_DETECTED=`ls /var/www/redcap | grep redcap_v | cut -d 'v' -f2 | sort -n | tail -n 1`
    echo "$REDCAP_ZIP content indicates REDCap version: $REDCAP_VERSION_DETECTED"

    # STEP 1: Create a MySQL database/schema and user
    create_redcap_database
    # STEP 2: Add MySQL connection values to 'database.php'
    update_redcap_connection_settings
    # STEP 3: simplify mysql connections with a .my.cnf file
    write_dot_mysql_dot_cnf
    # STEP 4: Create the REDCap database tables
    create_redcap_tables
    # STEP 5: Configure REDCap
    configure_redcap
    # STEP 6: Configure PHP
    configure_php_for_redcap
    configure_redcap_cron
    move_edocs_folder
}

function create_redcap_database() {
    echo "Creating database..."
    mysql <<SQL
DROP DATABASE IF EXISTS redcap;
CREATE DATABASE redcap;

GRANT
    SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, EXECUTE, CREATE VIEW, SHOW VIEW
ON
    redcap.*
TO
    'redcap'@'localhost'
IDENTIFIED BY
    'password';
SQL
}

function update_redcap_connection_settings() {
    # edit redcap database config file (This needs to be done after extraction of zip files)
    echo "Setting the connection variables in: /var/www/redcap/database.php"
    echo '$hostname   = "localhost";' >> /var/www/redcap/database.php
    echo '$db         = "redcap";'    >> /var/www/redcap/database.php
    echo '$username   = "redcap";'    >> /var/www/redcap/database.php
    echo '$password   = "password";'  >> /var/www/redcap/database.php
    echo '$salt   = "abc";'  >> /var/www/redcap/database.php
}

function write_dot_mysql_dot_cnf() {
    # Write a .my.cnf file into the vagrant user's home dir
    echo "Writing ~/.my.cnf for vagrant user..."
    cat << EOF > /home/vagrant/.my.cnf
[mysql]
password=$DATABASE_PASSWORD
user=$DATABASE_USER
database=$DATABASE_NAME

[mysqldump]
password=$DATABASE_PASSWORD
user=$DATABASE_USER
EOF
    chown vagrant.vagrant /home/vagrant/.my.cnf

    echo "Writing ~/.my.cnf for root..."
    cat << EOF > ~/.my.cnf
[mysql]
password=$DATABASE_PASSWORD
user=$DATABASE_USER
database=$DATABASE_NAME

[mysqldump]
password=$DATABASE_PASSWORD
user=$DATABASE_USER
EOF

}


# Create tables from sql files distributed with redcap under
#  redcap_vA.B.C/Resources/sql/
#
# @see install.php for details
function create_redcap_tables() {
    echo "Creating REDCap tables..."
    SQL_DIR=/var/www/redcap/redcap_v$REDCAP_VERSION_DETECTED/Resources/sql
    mysql -uredcap -ppassword redcap < $SQL_DIR/install.sql
    mysql -uredcap -ppassword redcap < $SQL_DIR/install_data.sql
    mysql -uredcap -ppassword redcap -e "UPDATE redcap.redcap_config SET value = '$REDCAP_VERSION_DETECTED' WHERE field_name = 'redcap_version' "

    files=$(ls -v $SQL_DIR/create_demo_db*.sql)
    for i in $files; do
        echo "Executing sql file $i"
        mysql -uredcap -ppassword redcap < $i
    done
}

# Set REDCap settings for this dev instance of REDCap
function configure_redcap() {
    echo "Setting redcap_base_url to $redcap_base_url..."
    echo "update redcap_config set value='$redcap_base_url' where field_name = 'redcap_base_url';" | mysql
}

# Adjust PHP vars to match REDCap needs
function configure_php_for_redcap() {
    echo "Configuring php to match redcap needs..."
    php5_confd_for_redcap="/etc/php5/conf.d/90-settings-for-redcap.ini"
    echo "max_input_vars = $max_input_vars" > $php5_confd_for_redcap
    echo "upload_max_filesize = $upload_max_filesize" >> $php5_confd_for_redcap
    echo "post_max_size = $post_max_size" >> $php5_confd_for_redcap
}

# Turn on REDCap Cron
function configure_redcap_cron() {
    echo "Turning on REDCap Cron job..."
    crond_for_redcap=/etc/cron.d/redcap
    echo "# REDCap Cron Job (runs every minute)" > $crond_for_redcap
    echo "* * * * * root /usr/bin/php /var/www/redcap/cron.php > /dev/null" >> $crond_for_redcap
}

# move the edocs folder
function move_edocs_folder() {
    echo "Moving the edocs folder out of web space..."
    edoc_path="/var/edocs"
    default_edoc_path="/var/www/redcap/edocs"
    if [ ! -e $edoc_path ]; then
        if [ -e $default_edoc_path ]; then
            rsync -ar $default_edoc_path $edoc_path && rm -rf $default_edoc_path
        else
            mkdir $edoc_path
        fi
        # adjust the permissions on the new
        chown -R www-data.www-data $edoc_path
        find $edoc_path -type d | xargs -i chmod 775 {}
        find $edoc_path -type f | xargs -i chmod 664 {}
    fi
    mysql -e "UPDATE redcap.redcap_config SET value = '$edoc_path' WHERE field_name = 'edoc_path';"
}

# Check if the Apache server is actually serving the REDCap files
function check_redcap_status() {
    echo "Checking if redcap application is running..."
    curl -s http://localhost/redcap/ | grep -i 'Welcome\|Critical Error'
    echo "Please try to login to REDCap as user 'admin' and password: 'password'"
}

function install_utils() {
    echo "Installing utilities..."
    cp $SHARED_FOLDER/aliases /home/vagrant/.bash_aliases
}

function configure_exim4() {
    echo "Configuring exim4..."
cat << EOF > /etc/exim4/update-exim4.conf.conf
dc_eximconfig_configtype='satellite'
dc_other_hostnames='localhost'
dc_local_interfaces='127.0.0.1 ; ::1'
dc_readhost='$development_hostname'
dc_relay_domains=''
dc_minimaldns='false'
dc_relay_nets=''
dc_smarthost='$smtp_smarthost'
CFILEMODE='644'
dc_use_split_config='false'
dc_hide_mailname='true'
dc_mailname_in_oh='true'
dc_localdelivery='mail_spool'
EOF

cat << EOF > /etc/aliases
mailer-daemon: postmaster
postmaster: root
nobody: root
hostmaster: root
usenet: root
news: root
webmaster: root
www: root
ftp: root
abuse: root
noc: root
security: root
root: vagrant
EOF

cat << EOF > /etc/mailname
$development_hostname
EOF

service exim4 restart

}

function configure_php_mail() {
    echo "Configuring php mail..."
    sed -e "sX.*sendmail_path.*Xsendmail_path = /usr/sbin/sendmail -t -iX;" -i /etc/php5/apache2/php.ini
    sed -e "sX.*mail.log.*Xmail.log = syslogX;" -i /etc/php5/apache2/php.ini
}
