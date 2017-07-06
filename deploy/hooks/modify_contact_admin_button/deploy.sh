#!/bin/bash
set -e

export MYTARGETDIR=$1
MYHOOK=$MYTARGETDIR/redcap_every_page_top

# determine the directory where this script resides
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# get source files
TEMPDIR=`mktemp -d`
git clone ssh://git@ctsit-forge.ctsi.ufl.edu/modify_contact_admin_button.git $TEMPDIR

# copy files to the correct target locations
mkdir -p $MYHOOK
cp $TEMPDIR/modify_contact_admin_button.php $MYHOOK

rm -rf $TEMPDIR
