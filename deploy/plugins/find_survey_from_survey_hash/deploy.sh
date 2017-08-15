#!/bin/bash
set -e

export MYTARGETDIR=$1

# determine the directory where this script resides
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# get source files
TEMPDIR=`mktemp -d`
git clone ssh://git@ctsit-forge.ctsi.ufl.edu/find_survey_from_survey_hash.git $TEMPDIR

# copy files to the correct target locations
mkdir -p $MYTARGETDIR
cp $TEMPDIR/index.php $MYTARGETDIR
cp $TEMPDIR/README.md $MYTARGETDIR

rm -rf $TEMPDIR
