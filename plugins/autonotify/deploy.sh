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

# Make a directory for supplementary SSL configuration details
SSL_INCLUDES=/etc/apache2/ssl-includes
if [ ! -e $SSL_INCLUDES ]; then
    mkdir -p $SSL_INCLUDES
fi

# make sure the above SSL_INCLUDES directory is referenced in the apache ssl config
SSL_CONFIG=/etc/apache2/sites-available/default-ssl.conf
if [ -e $SSL_CONFIG ]; then
    if [ `grep -c "Include ssl-includes/" $SSL_CONFIG` == 0 ] ; then
        echo "WARNING: the line 'Include ssl-includes/' does not existing in $SSL_CONFIG.  Please fix this."
    fi
else
    echo "Error: I don't know where the SSL configuration file is.  Exiting!"
    exit
fi

# place our apache directives in the SSL_INCLUDES directory
if [ ! $SHIB == "0" ]; then
    cp $DIR/autonotify.conf $SSL_INCLUDES/
    service apache2 restart
fi

# Alert the admin to turn on DET for the REDCAP system
echo "$DIR: Please turn on DET for this REDCap instance"
