# Hook Deployment

The document describes how REDCap Hooks are deployed on CTSI REDCap instances.

## Where do we get hooks?

CTS-IT installs REDCap deploys hooks exclusively from the REDCap-Extras repository:
[REDCap Extras](https://github.com/ctsit/redcap-extras.git)

These hooks must be deployed into the REDCap instance, and should be selectively
activated. Activations can be global or project specific.

## Deployment

Hooks are deployed with the script ./deploy_extensions.sh.  More specifically,
the function _deploy\_hooks_ in deployment_functions.sh does the hook
deployment.

deploy_hooks requires a data file as input to indicate the scope of the
script, which hook will trigger it and the relative path to the script. A
sample input file would look like this:

    PROJECT_ID,HOOK,SCRIPT_PATH
    pid333,redcap_data_entry_form,library/redcap_data_entry_form/complex_validation.php
    ,redcap_data_entry_form,library/redcap_data_entry_form/some_other_cool_feature.php

The activated hook list for the CTSI REDCap servers are in ./hooks/\<INSTANCE_NAME\> in this repo. Current that content is:

    redcap.ctsi.ufl.edu
    redcapstage.ctsi.ufl.edu

Deploy_hooks will copy all the needed files from the redcap-extras repo to
the hooks/library folder of the REDCap instance. It will then activate hooks based on contents of the file ./hooks/\<INSTANCE_NAME\>data.csv.

By default, it uses the UF CTSI production data for hook activation. To change this, specify an alternative configuration by exporting these 3 variables:

    REDCAP_ROOT - the full path to the Apache document root of your redcap server
    REDCAP_HOOKS - the full path the to hooks folder under $REDCAP_ROOT
    HOOKS_CONFIGURATION - the name of the directory ./hooks/\<INSTANCE_NAME\> that has the correct data.csv

e.g.

    export REDCAP_ROOT=/var/https/redcap
    export REDCAP_HOOKS=$REDCAP_ROOT/hooks
    export HOOKS_CONFIGURATION=redcap.ctsi.ufl.edu


## Activate the hooking mechanism

REDCap requires the hooking mechanism be activated in the Control Center.
This is a system-wide setting.  The REDCap hooking mechanism must be activated
by setting the Control Center -> General Configuration -> REDCap Hooks to the path to the redcap\_hooks.php file deployed by this repo.  For UF CTSI, this path is _/var/https/redcap/hooks/redcap\_hooks.php_


### Details

Generic activation instructions can be found at [Extensible REDCap
Hooks](https://github.com/ctsit/redcap-extras/blob/develop/hooks/README.md).

The hooks library is deployed to the folder $REDCAP_ROOT/hooks/library

The main REDCap hook function is deployed to $REDCAP_ROOT/hooks/redcap\_hooks.php

Global REDCap hooks are sym linked from the library to $REDCAP_ROOT/hooks/$HOOKNAME/scriptname.php

Project specific hooks are sym linked from the library to $REDCAP_ROOT/hooks/pid$project\_id/$HOOKNAME/scriptname.php
