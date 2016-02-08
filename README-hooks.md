# Hook Deployment

The document describes how REDCap Hooks are deployed on CTSI REDCap instances.

## Where do we get hooks?

CTS-IT installs REDCap deploys hooks exclusively from the REDCap-Extras repository:
[REDCap Extras](https://github.com/ctsit/redcap-extras.git)

These hooks must be deployed into the REDCap instance, and should be selectively
activated. Activations can be global or project specific.

## Deployment

Hooks are deployed with the script ./deploy_hooks.sh from the repo ssh://git
@ctsit-forge.ctsi.ufl.edu/redcap\_deployment.git.

deploy_hooks.php requires a data file as input to indicate the scope of the
script, which hook will trigger it and the relative path to the script. A
sample input file would look like this:

    PROJECT_ID,HOOK,SCRIPT_PATH
    pid333,redcap_data_entry_form,library/redcap_data_entry_form/complex_validation.php
    ,redcap_data_entry_form,library/redcap_data_entry_form/some_other_cool_feature.php

The activated hook list for the CTSI REDCap servers are in ./hooks/\<INSTANCE_NAME\> in this repo. Current that content is:

    redcap.ctsi.ufl.edu
    redcapstage.ctsi.ufl.edu

deploy_hooks.sh will copy all the needed files from the redcap-extras repo to
the hooks folder of the REDCap instance given the path to the appropriate data
file.  On the CTSI Prod instance, you could deploy with this command:

    sudo ./deploy_hooks.sh hooks/redcap.ctsi.ufl.edu/data.csv


## Activate the hooking mechanism

REDCap requires the hooking mechanism be activated in the Control Center.
This is a system-wide setting.  The REDCap hooking mechanism must be activated
by setting the Control Center -> General Configuration -> REDCap Hooks to
'/var/https/redcap/hooks/redcap_hooks.php'


### Details

Generic activation instructions can be found at [Extensible REDCap
Hooks](https://github.com/ctsit/redcap-extras/blob/develop/hooks/README.md).

The hooks library is deployed to the folder $REDCAP_ROOT/hooks/library

The main REDCap hook function is deployed to $REDCAP_ROOT/hooks/redcap\_hooks.php

Global REDCap hooks are sym linked from the library to $REDCAP_ROOT/hooks/$HOOKNAME/scriptname.php

Project specific hooks are sym linked from the library to $REDCAP_ROOT/hooks/pid$project\_id/$HOOKNAME/scriptname.php
