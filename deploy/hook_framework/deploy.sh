#!/bin/bash
set -e

export MYTARGETDIR=$1

# determine the directory where this script resides
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# get source files
TEMPDIR=`mktemp -d`
git clone https://github.com/vanderbilt/redcap-external-modules.git $TEMPDIR

# copy files to the correct target locations
mkdir -p $MYTARGETDIR/external_modules
cp -r $TEMPDIR/* $MYTARGETDIR/external_modules

rm -rf $TEMPDIR
