#!/bin/bash
set -e

export MYTARGETDIR=$1

# determine the directory where this script resides
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# get source files
TEMPDIR=`mktemp -d`
git clone ssh://git@ctsit-forge.ctsi.ufl.edu/linear_data_entry_workflow.git $TEMPDIR

# If you need to checkout code from another branch, uncomment and adjust this line
git --git-dir=$TEMPDIR/.git --work-tree=$TEMPDIR checkout develop

# copy files to the correct target locations
HOOK_FUNCTION_DIR=$MYTARGETDIR/redcap_data_entry_form
mkdir -p $HOOK_FUNCTION_DIR
cp $TEMPDIR/copy_values_from_previous_event.php $HOOK_FUNCTION_DIR
cp $TEMPDIR/force_data_entry_constraints.php $HOOK_FUNCTION_DIR
cp $TEMPDIR/default_from_field.php $HOOK_FUNCTION_DIR

HOOK_FUNCTION_DIR=$MYTARGETDIR/redcap_every_page_top
mkdir -p $HOOK_FUNCTION_DIR
cp $TEMPDIR/rfio_dashboard.php $HOOK_FUNCTION_DIR
cp $TEMPDIR/rfio_data_entry.php $HOOK_FUNCTION_DIR
cp $TEMPDIR/rfio_record_home.php $HOOK_FUNCTION_DIR
cp $TEMPDIR/default_from_field_help.php $HOOK_FUNCTION_DIR

rm -rf $TEMPDIR
