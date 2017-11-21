#!/bin/bash
set -e

export MYTARGETDIR=$1

# get source files
TEMPDIR=`mktemp -d`
git clone https://github.com/vanderbilt/redcap-external-modules.git $TEMPDIR

# copy files to the correct target locations
mkdir -p $MYTARGETDIR
cp -r $TEMPDIR/* $MYTARGETDIR

rm -rf $TEMPDIR
