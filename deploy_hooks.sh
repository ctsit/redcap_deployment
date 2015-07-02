#!/bin/bash

export REDCAP_ROOT=/var/https/redcap
export REDCAP_HOOKS=$REDCAP_ROOT/hooks
export INPUT=$1

if [ ! -e $REDCAP_ROOT ]; then
    echo "Error: REDCAP_ROOT, $REDCAP_ROOT, does not exist.  Exiting."
    exit
fi
if [ ! -e $REDCAP_HOOKS ]; then
    mkdir $REDCAP_ROOT/hooks
    echo "REDCap Hooks Directory Created."
    exit
fi

# Pull repo and copy scripts into library folder
MYTEMP=`mktemp -d`
cd $MYTEMP
git clone https://github.com/ctsit/redcap-extras.git
if [ ! -e redcap-extras ]; then
    echo "Error: redcap-extras repo could not be cloned. Exiting."
    exit
fi
cd redcap-extras/hooks

# checkout develop because we have not yet released the code we need
git checkout develop
cp redcap_hooks.php $REDCAP_HOOKS/
mkdir $REDCAP_HOOKS/library
cp -r examples/* $REDCAP_HOOKS/library/
rm -rf $MYTEMP

# Make required directories for hook deployment
awk -F"," 'NR!=1{printf "mkdir -p %s/%s/%s/\n",ENVIRON["REDCAP_HOOKS"],$1,$2}' $INPUT | sh

# Create sym links for hooks to be executed
awk -F"," 'NR!=1{printf "ln -s %s/%s %s/%s/%s/\n",ENVIRON["REDCAP_HOOKS"],$3,ENVIRON["REDCAP_HOOKS"],$1,$2}' $INPUT | sh
