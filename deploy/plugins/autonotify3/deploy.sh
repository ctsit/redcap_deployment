#!/bin/bash
set -e

export MYTARGETDIR=$1

# determine the directory where this script resides
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# get source files
TEMPDIR=`mktemp -d`
git clone https://github.com/pbchase/redcap-autonotify3.git $TEMPDIR

# copy files to the correct target locations
mkdir -p $MYTARGETDIR
cp $TEMPDIR/index.php $MYTARGETDIR
cp $TEMPDIR/common.php $MYTARGETDIR
cp $TEMPDIR/Utility.php $MYTARGETDIR
cp $TEMPDIR/cron.php $MYTARGETDIR
cp $TEMPDIR/EnhancedPiping.php $MYTARGETDIR

rm -rf $TEMPDIR
