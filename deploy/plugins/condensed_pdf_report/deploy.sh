#!/bin/bash
set -e

export MYTARGETDIR=$1

# determine the directory where this script resides
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# copy files to the correct target locations
mkdir -p $MYTARGETDIR
cp $DIR/index.php $MYTARGETDIR
cp $DIR/ORIGIN.md $MYTARGETDIR

echo "$DIR: Access the PDF Modified Report plugin at /redcap/plugins/condensed_pdf_report/"
