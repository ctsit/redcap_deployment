#!/bin/bash
set -e

export MYTARGETDIR=$1

# download composer installer
TEMPDIR=`mktemp -d`
php -r "copy('https://getcomposer.org/installer', '$TEMPDIR/composer-setup.php');"

# install composer
php $TEMPDIR/composer-setup.php --install-dir=$TEMPDIR

# install dependencies
cp composer.json $TEMPDIR
COMPOSER=$TEMPDIR/composer.json $TEMPDIR/composer.phar install -d $TEMPDIR

# removing install files
rm $TEMPDIR/composer-setup.php
rm $TEMPDIR/composer.phar

# copying composer.json, composer.lock and vendor folder to the final location
cp -r $TEMPDIR/* $MYTARGETDIR

# removing temporary folder
rm -rf $TEMPDIR
