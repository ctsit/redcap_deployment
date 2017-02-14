#!/bin/bash
set -e

export MYTARGETDIR=$1

# determine the directory where this script resides
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# get source files
TEMPDIR=`mktemp -d`
git clone https://github.com/123andy/redcap-custom-dashboard.git $TEMPDIR

# copy files to the correct target locations
mkdir -p $MYTARGETDIR
cp $TEMPDIR/index.php $MYTARGETDIR
cp $TEMPDIR/custom_dashboard.js $MYTARGETDIR

rm -rf $TEMPDIR
