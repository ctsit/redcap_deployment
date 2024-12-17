#!/bin/bash
set -e

export MYTARGETDIR=$1

cp composer.json $MYTARGETDIR
cd $MYTARGETDIR

# download composer installer
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"

# install composer
php composer-setup.php

# install dependencies
php composer.phar install

# removing install files
rm composer-setup.php
rm composer.phar
