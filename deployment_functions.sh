#!/bin/bash

# Contributors:
#    Philip Chase <philipbchase@gmail.com>
#    Erik Schmidt <cavedivr@ufl.edu>

# Copyright (c) 2015, University of Florida
# All rights reserved.
#
# Distributed under the BSD 3-Clause License
# For full text of the BSD 3-Clause License see http://opensource.org/licenses/BSD-3-Clause


# REDCap Deployment Functions

function deploy_hooks() {
    if [ ! -e $REDCAP_HOOKS ]; then
        mkdir -p $REDCAP_HOOKS
        echo "REDCap Hooks Directory Created."
    fi

    # Pull repo with our hooks and copy scripts into library folder
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
    if [ ! -e $REDCAP_HOOKS/library ]; then
        mkdir $REDCAP_HOOKS/library
        echo "REDCap Hooks Library Directory Created."
    fi
    if [ -e library ]; then
        cp -r library/* $REDCAP_HOOKS/library/
    elif [ -e examples ]; then
        cp -r examples/* $REDCAP_HOOKS/library/
    else
        echo "Error: Source directory for library files not found.  Could not copy files to $REDCAP_HOOKS/library/"
        exit
    fi
    cd $SCRIPT_DIR
    rm -rf $MYTEMP

    # Make required directories for hook deployment
    echo "Making required directories for hook deployment based on content from $SCRIPT_DIR/hooks/$HOOKS_CONFIGURATION ..."
    awk -F"," 'NR!=1{printf "mkdir -p %s/%s/%s/\n",ENVIRON["REDCAP_HOOKS"],$1,$2}' $SCRIPT_DIR/hooks/$HOOKS_CONFIGURATION/data.csv | sh

    # Create sym links for hooks to be executed
    echo "Creating symbolic links for hooks to be executed based on content from $SCRIPT_DIR/hooks/$HOOKS_CONFIGURATION..."
    awk -F"," 'NR!=1{printf "ln -sf %s/%s %s/%s/%s/\n",ENVIRON["REDCAP_HOOKS"],$3,ENVIRON["REDCAP_HOOKS"],$1,$2}' $SCRIPT_DIR/hooks/$HOOKS_CONFIGURATION/data.csv | sh
}

function deploy_plugins() {
    export REDCAP_PLUGINS=$REDCAP_ROOT/plugins
    if [ ! -e $REDCAP_PLUGINS ]; then
        mkdir -p $REDCAP_PLUGINS
        echo "REDCap plugins directory, $REDCAP_PLUGINS, created."
    fi

    # copy each plugin to the target, deploy, and test
    cd $SCRIPT_DIR/plugins/
    for PLUGIN in `find . -maxdepth 1 -type d | grep /`
    do
        cd $SCRIPT_DIR/plugins/
        echo "Deploying $PLUGIN plugin to $REDCAP_PLUGINS/$PLUGIN/..."
        if [ ! -e $REDCAP_PLUGINS/$PLUGIN ]; then
            echo "Creating directory $REDCAP_PLUGINS/$PLUGIN..."
            mkdir -p $REDCAP_PLUGINS/$PLUGIN
        fi

        # Run deployment script if any
        cd $SCRIPT_DIR/plugins/
        if [ -e $PLUGIN/deploy.sh ]; then
            echo "Deploying via $PLUGIN/deploy.sh..."
            bash $PLUGIN/deploy.sh $REDCAP_PLUGINS/$PLUGIN/
        else
            # just copy all the files if there is no deployment script
            echo "Rsyncing files for $PLUGIN"
            rsync -arc $PLUGIN/ $REDCAP_PLUGINS/$PLUGIN/
        fi

        # Run test script if any
        cd $SCRIPT_DIR/plugins/
        if [ -e $PLUGIN/test.sh ]; then
            echo "Testing via $PLUGIN/test.sh..."
            bash $PLUGIN/test.sh $REDCAP_PLUGINS/$PLUGIN/
        fi
    done
}
