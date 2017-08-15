#!/bin/bash
set -e

export MYTARGETDIR=$1

# determine the directory where this script resides
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# get source files
TEMPDIR=`mktemp -d`
git clone git@github.com:ctsit/custom_project_settings.git $TEMPDIR

# copy files to the correct target locations
mkdir -p $MYTARGETDIR
cp $TEMPDIR/cps.php $MYTARGETDIR
cp $TEMPDIR/cps_lib.php $MYTARGETDIR
cp $TEMPDIR/delete.php $MYTARGETDIR
cp $TEMPDIR/index.php $MYTARGETDIR
cp $TEMPDIR/submit.php $MYTARGETDIR


rm -rf $TEMPDIR
