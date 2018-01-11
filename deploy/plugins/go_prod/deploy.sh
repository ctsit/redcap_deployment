#!/bin/bash
set -e

export MYTARGETDIR=$1

# determine the directory where this script resides
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# get source files
TEMPDIR=`mktemp -d`
git clone https://github.com/aandresalvarez/go_to_prod.git $TEMPDIR

# copy files to the correct target locations
mkdir -p $MYTARGETDIR
cp $TEMPDIR/index.php $MYTARGETDIR
cp $TEMPDIR/README.md $MYTARGETDIR
cp -r $TEMPDIR/classes $MYTARGETDIR
cp $TEMPDIR/gotoprod.gif $MYTARGETDIR
cp -r $TEMPDIR/js $MYTARGETDIR
cp -r $TEMPDIR/settings $MYTARGETDIR
cp -r $TEMPDIR/styles $MYTARGETDIR
cp -r $TEMPDIR/views $MYTARGETDIR

rm -rf $TEMPDIR
