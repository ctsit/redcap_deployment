#!/bin/bash

# Contributors:
#    Christopher P. Barnes <senrabc@gmail.com>
#    Andrei Sura: github.com/indera
#    Mohan Das Katragadda <mohan.das142@gmail.com>
#    Philip Chase <philipbchase@gmail.com>
#    Ruchi Vivek Desai <ruchivdesai@gmail.com>
#    Taeber Rapczak <taeber@ufl.edu>
#    Josh Hanna <josh@hanna.io>
#
# Copyright (c) 2016, University of Florida
# All rights reserved.
#
# Distributed under the BSD 3-Clause License
# For full text of the BSD 3-Clause License see http://opensource.org/licenses/BSD-3-Clause

function log() {
    echo -n "MSG: "
    echo $*
}

function install_utils() {
    log "Executing ${FUNCNAME[0]}"
    apt-get install -y git vim ack-grep unzip \
        tree colordiff libxml2-utils xmlstarlet nmap

    chown -R vagrant.vagrant /home/vagrant
}

function install_prereqs() {
    log "Executing ${FUNCNAME[0]}"
    REQUIRED_PARAMETER_COUNT=2
    if [ $# != $REQUIRED_PARAMETER_COUNT ]; then
        echo "${FUNCNAME[0]} Installs and configures MySQL, Apache and php7"
        echo "${FUNCNAME[0]} requires these $REQUIRED_PARAMETER_COUNT parameters in this order:"
        echo "MYSQL_REPO           The MySQL Repo to install from.  E.g., mysql-5.6"
        echo "DATABASE_ROOT_PASS   Password of the MySQL root user."
        return 1
    else
        MYSQL_REPO=$1
        DATABASE_ROOT_PASS=$2
    fi


    # Try two different keyservers to get the MySQL repository key
    gpg --keyserver pgp.mit.edu --recv-keys 5072E1F5 || gpg --keyserver sks-keyservers.net --recv-keys 5072E1F5
    gpg -a --export 5072E1F5 | apt-key add -

cat << END > /etc/apt/sources.list.d/mysql.list
deb http://repo.mysql.com/apt//debian/ jessie $MYSQL_REPO
deb-src http://repo.mysql.com/apt//debian/ jessie $MYSQL_REPO
END

    log "Adding php7 repo to prepare for installation..."
    echo 'deb http://packages.dotdeb.org jessie all' >> /etc/apt/sources.list
    echo 'deb-src http://packages.dotdeb.org jessie all' >> /etc/apt/sources.list
    wget --no-check-certificate -q -O - https://www.dotdeb.org/dotdeb.gpg | apt-key add -

    apt-get update

    log "Preparing to install mysql-community-server with root password: '$DATABASE_ROOT_PASS'..."
    echo mysql-server mysql-server/root_password       password $DATABASE_ROOT_PASS | debconf-set-selections
    echo mysql-server mysql-server/root_password_again password $DATABASE_ROOT_PASS | debconf-set-selections
    echo mysql-community-server mysql-community-server/root_password       password $DATABASE_ROOT_PASS | debconf-set-selections
    echo mysql-community-server mysql-community-server/root_password_again password $DATABASE_ROOT_PASS | debconf-set-selections
    echo mysql-community-server mysql-community-server/root-pass           password $DATABASE_ROOT_PASS | debconf-set-selections
    echo mysql-community-server mysql-community-server/re-root-pass        password $DATABASE_ROOT_PASS | debconf-set-selections

    apt-get install -y apache2
    apt-get install -y mysql-community-server

    log "Installing php7 and required dependencies..."
    apt-get -y install php7.0
    apt-get -y install php7.0-xml
    apt-get -y install libapache2-mod-php7.0 php7.0-mysql php7.0-curl php7.0-json
    service apache2 restart

    # Configure mysqld to be more permissive
    log "Configure mysqld to be more permissive..."
    MYSQLCONF=/etc/mysql/my.cnf
    echo '' >> $MYSQLCONF
    echo '[mysqld]' >> $MYSQLCONF
    echo 'sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' >> $MYSQLCONF
    service mysql restart

    # configure MySQL to start every time
    update-rc.d mysql defaults

    # Increase the default upload size limit to allow ginormous files
    sed -i 's/upload_max_filesize =.*/upload_max_filesize = 20M/' /etc/php/7.0/apache2/php.ini
    sed -i 's/;date.timezone =.*/date.timezone = America\/New_York/' /etc/php/7.0/apache2/php.ini
    sed -i 's/;date.timezone =.*/date.timezone = America\/New_York/' /etc/php/7.0/cli/php.ini

    log "Stop apache..."
    service apache2 stop
    # Keep the default site on port :80
    # a2dissite 000-default

    log "Link config files for apache port 443"
    find /etc/apache2/sites-* | xargs -i ls -l {}
    cp /vagrant/files/apache-ssl.conf /etc/apache2/sites-available/default-ssl.conf
    ln -sfv /etc/apache2/sites-available/default-ssl.conf /etc/apache2/sites-enabled/apache-ssl.conf

    log "Link config files for apache port 80"
    OLD_APACHE_DEFAULT=/etc/apache2/sites-enabled/000-default.conf
    if [ -e $OLD_APACHE_DEFAULT ]; then rm $OLD_APACHE_DEFAULT; fi

    OLD_APACHE_DEFAULT=/etc/apache2/sites-available/000-default.conf
    if [ -e $OLD_APACHE_DEFAULT ]; then rm $OLD_APACHE_DEFAULT; fi

    cp /vagrant/files/apache-default.conf /etc/apache2/sites-available/000-default.conf
    ln -sfv /etc/apache2/sites-available/000-default.conf  /etc/apache2/sites-enabled/000-default.conf

    cp /vagrant/files/ssl.conf /etc/apache2/mods-available/ssl.conf

    log "Enable apache modules"
    a2enmod ssl
    a2enmod rewrite

    log "Restarting apache with new config..."
    sleep 2
    service apache2 start
}

function create_database() {
    log "Executing ${FUNCNAME[0]}"

    REQUIRED_PARAMETER_COUNT=5
    if [ $# != $REQUIRED_PARAMETER_COUNT ]; then
        echo "${FUNCNAME[0]} Creates a MySQL database, a DB user with access to the DB, and sets user's password."
        echo "${FUNCNAME[0]} requires these $REQUIRED_PARAMETER_COUNT parameters in this order:"
        echo "DATABASE_NAME        Name of the database to create"
        echo "DATABASE_USER        Database user who will have access to DATABASE_NAME"
        echo "DATABASE_PASSWORD    Password of DATABASE_USER"
        echo "DATABASE_HOST        The host from which DATABASE_USER is authorized to access DATABASE_NAME"
        echo "DATABASE_ROOT_PASS   Password of the mysql root user"
        return 1
    else
        DATABASE_NAME=$1
        DATABASE_USER=$2
        DATABASE_PASSWORD=$3
        DATABASE_HOST=$4
        DATABASE_ROOT_PASS=$5
    fi

    log "Creating database $DATABASE_NAME"
    # Create database used by the app
    mysql -u root -p$DATABASE_ROOT_PASS mysql <<SQL
DROP DATABASE IF EXISTS $DATABASE_NAME;
CREATE DATABASE $DATABASE_NAME;

GRANT
    SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, EXECUTE, CREATE VIEW, SHOW VIEW
ON
    $DATABASE_NAME.*
TO
    '$DATABASE_USER'@'$DATABASE_HOST'
IDENTIFIED BY
    '$DATABASE_PASSWORD';
SQL

    # grant access to $DATABASE_USER@% so the VM host can access mysql on port 3306
    mysql -u root -p$DATABASE_ROOT_PASS mysql <<SQL
GRANT
    SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, EXECUTE, CREATE VIEW, SHOW VIEW
ON
    $DATABASE_NAME.*
TO
    '$DATABASE_USER'@'%'
IDENTIFIED BY
    '$DATABASE_PASSWORD';
SQL

}

function update_cake_connection_settings() {
    log "Executing ${FUNCNAME[0]}"

    REQUIRED_PARAMETER_COUNT=4
    if [ $# != $REQUIRED_PARAMETER_COUNT ]; then
        echo "${FUNCNAME[0]} Rewrites the CakePHP database.php for this app."
        echo "${FUNCNAME[0]} requires these $REQUIRED_PARAMETER_COUNT parameters in this order:"
        echo "DEPLOY_DIR           The directory where the app is deployed"
        echo "DATABASE_USER        Database user who will have access to DATABASE_NAME"
        echo "DATABASE_PASSWORD    Password of DATABASE_USER"
        echo "DATABASE_HOST        The host from which DATABASE_USER is authorized to access DATABASE_NAME"
        return 1
    else
        DEPLOY_DIR=$1
        DATABASE_USER=$2
        DATABASE_PASSWORD=$3
        DATABASE_HOST=$4
    fi

    # edit cake database config file
    CAKE_DB_CONFIG_FILE=$DEPLOY_DIR/app/Config/database.php
    echo "Setting the connection variables in: $CAKE_DB_CONFIG_FILE"
    sed -e "s/'host'.*=>.*/'host' => '$DATABASE_HOST',/;" -i $CAKE_DB_CONFIG_FILE
    sed -e "s/'login'.*=>.*/'login' => '$DATABASE_USER',/;" -i $CAKE_DB_CONFIG_FILE
    sed -e "s/'password'.*=>.*/'password' => '$DATABASE_PASSWORD',/;" -i $CAKE_DB_CONFIG_FILE
    #sed -e "s/'database'.*=>.*/'database' => '$DATABASE_NAME',/;" -i $CAKE_DB_CONFIG_FILE
}

function write_dot_mysql_dot_cnf() {
    log "Executing ${FUNCNAME[0]}"
    REQUIRED_PARAMETER_COUNT=4
    if [ $# != $REQUIRED_PARAMETER_COUNT ]; then
        echo "${FUNCNAME[0]} Creates .my.cnf files for vagrant user and root."
        echo "${FUNCNAME[0]} requires these $REQUIRED_PARAMETER_COUNT parameters in this order:"
        echo "DATABASE_NAME        Name of the database to access."
        echo "DATABASE_USER        Database user to connect with."
        echo "DATABASE_PASSWORD    Password of DATABASE_USER"
        echo "DATABASE_ROOT_PASS   Password of root MySQL user"
        return 1
    else
        DATABASE_NAME=$1
        DATABASE_USER=$2
        DATABASE_PASSWORD=$3
        DATABASE_ROOT_PASS=$4
    fi

    # Write a .my.cnf file into the vagrant user's home dir
    cat << EOF > /home/vagrant/.my.cnf
[mysql]
password="$DATABASE_PASSWORD"
user=$DATABASE_USER
database=$DATABASE_NAME

[mysqldump]
password="$DATABASE_PASSWORD"
user=$DATABASE_USER
EOF
    chown vagrant.vagrant /home/vagrant/.my.cnf

    # Write a .my.cnf file into the root's home dir
    cat << EOF > /root/.my.cnf
[mysql]
password="$DATABASE_ROOT_PASS"
user=root
database=$DATABASE_NAME

[mysqldump]
password="$DATABASE_ROOT_PASS"
user=root
EOF
}

function populate_db () {
    log "Executing ${FUNCNAME[0]}"
    REQUIRED_PARAMETER_COUNT=5
    if [ $# != $REQUIRED_PARAMETER_COUNT ]; then
        echo "${FUNCNAME[0]} Creates a MySQL database, a DB user with access to the DB, and sets user's password."
        echo "${FUNCNAME[0]} requires these $REQUIRED_PARAMETER_COUNT parameters in this order:"
        echo "DATABASE_NAME        Name of the database to create"
        echo "DATABASE_USER        Database user who will have access to DATABASE_NAME"
        echo "DATABASE_PASSWORD    Password of DATABASE_USER"
        echo "DEPLOY_DIR           The directory where the app is deployed"
        echo "DB_EPOCH_VERSION     The version of the schema files to be loaded before applying upgrades"
        return 1
    else
        DATABASE_NAME=$1
        DATABASE_USER=$2
        DATABASE_PASSWORD=$3
        DEPLOY_DIR=$4
        DB_EPOCH_VERSION=$5
    fi

    SCHEMA_FOLDER=$DEPLOY_DIR/schema

    # LOad the three epoch files--schema.sql, data_minimal.sql and data_testing.sql--in that order
    for file in schema.sql data_minimal.sql data_testing.sql ; do
        create_tables $DATABASE_NAME $DATABASE_USER $DATABASE_PASSWORD $SCHEMA_FOLDER/$DB_EPOCH_VERSION/$file
    done

    # load every upgrade.sql with a higher version number than the $DB_EPOCH_VERSION
    for dir in `find $SCHEMA_FOLDER -maxdepth 1 -type d | sort --version-sort | grep -A1000 $DB_EPOCH_VERSION | tail -n +2` ; do
        if [ -e $dir/upgrade.sql ]; then
            create_tables $DATABASE_NAME $DATABASE_USER $DATABASE_PASSWORD $dir/upgrade.sql
        fi
    done

}

function create_tables() {
    log "Executing: create_tables()"
    # load a single SQL file into the database to initialize the application

    REQUIRED_PARAMETER_COUNT=4
    if [ $# != $REQUIRED_PARAMETER_COUNT ]; then
        echo "${FUNCNAME[0]} Creates a MySQL database, a DB user with access to the DB, and sets user's password."
        echo "${FUNCNAME[0]} requires these $REQUIRED_PARAMETER_COUNT parameters in this order:"
        echo "DATABASE_NAME        Name of the database to create"
        echo "DATABASE_USER        Database user who will have access to DATABASE_NAME"
        echo "DATABASE_PASSWORD    Password of DATABASE_USER"
        echo "SQL_FILE             The full path to the SQL file that will be loaded into the DATABASE_NAME"
        return 1
    else
        DATABASE_NAME=$1
        DATABASE_USER=$2
        DATABASE_PASSWORD=$3
        SQL_FILE=$4
    fi

    if [ -e $SQL_FILE ]; then
        echo "Loading database file $SQL_FILE into $DATABASE_NAME..."
        mysql -u$DATABASE_USER -p$DATABASE_PASSWORD $DATABASE_NAME < $SQL_FILE
    else
        echo "Database file $SQL_FILE does not exist"
    fi
}

function install_xdebug() {
    # Install XDebug for enabling code coverage
    log "Executing: install_xdebug()"
    apt-get install php7.0-xdebug

    echo 'Restarting apache server'
    service apache2 restart
}

function install_composer_deps() {
    log "Executing: install_composer_deps()"
    REQUIRED_PARAMETER_COUNT=1
    if [ $# != $REQUIRED_PARAMETER_COUNT ]; then
        echo "${FUNCNAME[0]} Installs PHP Composer and runs 'composer install' for this app"
        echo "${FUNCNAME[0]} requires these $REQUIRED_PARAMETER_COUNT parameters in this order:"
        echo "DEPLOY_DIR           The directory where the app is deployed"
        return 1
    else
        DEPLOY_DIR=$1
    fi

    curl -sS https://getcomposer.org/installer | php
    mv composer.phar /usr/local/bin/composer

    pushd $DEPLOY_DIR/app
        # silence the deprecation notice
        # The Composer\Package\LinkConstraint\VersionConstraint class is deprecated,
        # use Composer\Semver\Constraint\Constraint instead. in phar:///usr/local/bin/composer/src/Composer/Package/LinkConstraint/VersionConstraint.php:17
        phpdismod xdebug
        composer install 2>&1 | tee ~/log_install_composer_deps
        phpenmod xdebug
    popd
    log "Done with install_composer_deps()"
}

function upgrade_acl () {
    echo "Executing: upgrade_acl()"

    REQUIRED_PARAMETER_COUNT=2
    if [ $# != $REQUIRED_PARAMETER_COUNT ]; then
        echo "${FUNCNAME[0]} Runs any ACL Upgrade scripts"
        echo "${FUNCNAME[0]} requires these $REQUIRED_PARAMETER_COUNT parameters in this order:"
        echo "DEPLOY_DIR           The directory where the app is deployed"
        echo "DB_EPOCH_VERSION     The version of the schema files to be loaded before applying upgrades"
        return 1
    else
        DEPLOY_DIR=$1
        DB_EPOCH_VERSION=$2
    fi

    SCHEMA_FOLDER=$DEPLOY_DIR/schema

    # run every acl-upgrade.sh with a higher version number than the $DB_EPOCH_VERSION
    for dir in `find $SCHEMA_FOLDER -maxdepth 1 -type d | sort --version-sort | grep -A1000 $DB_EPOCH_VERSION | tail -n +2` ; do
        if [ -e $dir/acl-upgrade.sh ]; then
            echo "Running $dir/acl-upgrade.sh..."
            bash $dir/acl-upgrade.sh
        fi
    done

}

function reset_db {
    . /vagrant/.env
    create_database $DB $DB_APP_USER $DB_APP_PASSWORD $DB_HOST $DB_PASS
    create_database $DB_TEST $DB_APP_USER $DB_APP_PASSWORD $DB_HOST $DB_PASS
    update_cake_connection_settings $PATH_TO_APP_IN_GUEST_FILESYSTEM $DB_APP_USER $DB_APP_PASSWORD $DB_HOST
    populate_db $DB $DB_USER $DB_PASS $PATH_TO_APP_IN_GUEST_FILESYSTEM $DB_EPOCH_VERSION
    upgrade_acl $PATH_TO_APP_IN_GUEST_FILESYSTEM $DB_EPOCH_VERSION
}

function configure_exim4() {
    echo "Configuring exim4..."
cat << EOF > /etc/exim4/update-exim4.conf.conf
dc_eximconfig_configtype='satellite'
dc_other_hostnames='localhost'
dc_local_interfaces='127.0.0.1 ; ::1'
dc_readhost='$HOSTNAME_IN_HOST'
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
$HOSTNAME_IN_HOST
EOF

service exim4 restart

}

function configure_php_mail() {
    echo "Configuring php mail..."
    sed -e "sX.*sendmail_path.*Xsendmail_path = /usr/sbin/sendmail -t -iX;" -i /etc/php/7.0/apache2/php.ini
    sed -e "sX.*mail.log.*Xmail.log = syslogX;" -i /etc/php/7.0/apache2/php.ini
}

function install_pdftk() {
    echo "Installing PDF Toolkit..."
    apt-get install -y pdftk
}

function install_composer() {
  curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin
  mv /usr/local/bin/composer.phar /usr/local/bin/composer
  chmod 755 /usr/local/bin/composer
}
