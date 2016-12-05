#!/bin/bash

# Contributors:
#    Philip Chase <philipbchase@gmail.com>
#    Erik Schmidt <cavedivr@ufl.edu>

# Copyright (c) 2015, University of Florida
# All rights reserved.
#
# Distributed under the BSD 3-Clause License
# For full text of the BSD 3-Clause License see http://opensource.org/licenses/BSD-3-Clause

# Fail on first error
set -e

# use the same vagrant .env the guest was provisioned with
if [ -e /vagrant/.env ]; then
    . /vagrant/.env
fi

# make a note of where this script lives so we can use relative paths later
export SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Set defaults for required variables where they do not exist
REDCAP_ROOT=$PATH_TO_APP_IN_GUEST_FILESYSTEM
if [ -z "$REDCAP_ROOT" ]; then
    export REDCAP_ROOT=/var/https/redcap
fi

if [ -z "$REDCAP_HOOKS" ]; then
    export REDCAP_HOOKS=$REDCAP_ROOT/hooks
fi

if [ -z "$HOOKS_CONFIGURATION" ]; then
    export HOOKS_CONFIGURATION=redcap.ctsi.ufl.edu
fi

if [ ! -e $REDCAP_ROOT ]; then
    echo "Error: REDCAP_ROOT, $REDCAP_ROOT, does not exist.  Exiting."
    exit
fi

. $SCRIPT_DIR/deployment_functions.sh

deploy_plugins
