#!/bin/bash
set -e

export MYTARGETDIR=$1
MYHOOK=$MYTARGETDIR/redcap_every_page_top


# determine the directory where this script resides
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# get source files
TEMPDIR=`mktemp -d`
git clone ssh://git@ctsit-forge.ctsi.ufl.edu/redcap_custom_project_settings.git $TEMPDIR

# If you need to checkout code from another branch, uncomment and adjust this line
# git --git-dir=$TEMPDIR/.git --work-tree=$TEMPDIR checkout develop

# copy files to the correct target locations
mkdir -p $MYHOOK
cp $TEMPDIR/cps_hook.php $MYHOOK

rm -rf $TEMPDIR
