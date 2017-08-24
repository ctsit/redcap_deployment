#!/bin/bash
set -e

export MYTARGETDIR=$1

# download composer installer
TEMPDIR=`mktemp -d`
php -r "copy('https://getcomposer.org/installer', '$TEMPDIR/composer-setup.php');"
php -r "if (hash_file('SHA384', '$TEMPDIR/composer-setup.php') === '669656bab3166a7aff8a7506b8cb2d1c292f042046c5a994c43155c0be6190fa0355160742ab2e1c88d40d5be660b410') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('$TEMPDIR/composer-setup.php'); } echo PHP_EOL;"

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
