#!/bin/bash

# Utility to speed up deploying vagrant instances with fab for use in development of REDCap modules
# Allows use of bash auto-completion for deploying modules to vagrant vm

# Simple use: bash vague.sh modules/module_to_test/

# Suggested use:
# 1 make callable anywhere:
# 1.1 chmod +x vague.sh
# 1.2 cp vague.sh /usr/local/bin/vt
# 2 vt modules/module_to_test/

args=("$@")

# TODO: have user set a config file with the location of their redcap_deployment folder
# redcap_deployment_root_dir="/Users/kyle.chesney/projects/redcap_deployment"

if [[ $(pwd) =~ .*/redcap_deployment$ ]]; then
    is_in_root=true
fi

clone_module_directory () {
    # Clone module from elsewhere into the redcap_deploy modules directory to work with fab
    cp -r $1 ${redcap_deployment_root_dir}/modules
}

if [[ "$is_root" != true ]]; then
    # TODO: copy the module into redcap_deplyoment/modules/ and relocate
    echo "Please relocate to the redcap_deployment root directory"
    exit 1
    # clone_module_directory $1
    # cd $redcap_deployment_root_dir
fi

test_module () {
    t="$1"
    if [[ $1 =~ ^modules/* ]] ; then
        t="${1:8}" # remove "modules/" if calling from redcap_deploy root
    fi
    t=${t%?} # remove trailing / from autocomplete
	  fab vagrant test_module:$t
}
# If linking a module outside of redcap_deploymet/modules/, it copies the redcap_deployment/modules/ folder into another nested modules folder, and also includes the module there

test_module $1
