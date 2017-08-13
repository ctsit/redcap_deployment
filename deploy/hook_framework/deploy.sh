#!/bin/bash
set -e

export MYTARGETDIR=$1

# determine the directory where this script resides
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# get source files
TEMPDIR=`mktemp -d`
git clone https://github.com/tbembersimeao/xman.git $TEMPDIR
git --git-dir=$TEMPDIR/.git --work-tree=$TEMPDIR checkout develop

# copy files to the correct target locations
mkdir -p $MYTARGETDIR/xman
cp $TEMPDIR/.htaccess $MYTARGETDIR
cp -r $TEMPDIR/* $MYTARGETDIR/xman

rm -rf $TEMPDIR
