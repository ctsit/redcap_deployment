#!/bin/bash
set -e

export MYTARGETDIR=$1

cp composer.json $MYTARGETDIR
cd $MYTARGETDIR

# download composer installer
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"

# install composer
# pin to version 1.latest due to 2.x conflict: https://github.com/wikimedia/composer-merge-plugin/issues/184
php composer-setup.php --1

# install dependencies
php composer.phar install

# removing install files
rm composer-setup.php
rm composer.phar
