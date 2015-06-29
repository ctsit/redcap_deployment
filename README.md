# REDCap Deployment Scripts with added bonus... a Vagrant (will work for food)!

## BACKGROUND INFORMATION

This repo documents the scripts and tools used by CTS-IT for REDCap instance 
deployments and upgrades. A visitor to these regions should be able to understand
and complete the deployment process using the tools found here.

This repo also contains the mapping of hooks to specific project id's for the production
and staging instances of REDCap at the CTSI.

## REQUIREMENTS

A user of these tools will need to download and provide their own REDCap bits,
downloaded from Vanderbilt. This REDCap .zip should be placed in the /vagrant folder. 
It should not be renamed.

This VM requires that vagrant and virtual box be installed on the host system.

## UPGRADE

Upgrade instructions currently live in a Wiki article found here:
[CTS-IT Wiki Article on REDCap Upgrades](https://ctsit-forge.ctsi.ufl.edu/projects/redcap/wiki/REDCap_Upgrade_Instructions)

## INSTALLATION

We do not currently have a bare-metal installation procedure. That said, the vagrant
files presented in this repo contain many of the required steps in a deployment 
process. Other steps can be found in the above upgrade instructions.

## HOOK DEPLOYMENT

CST-IT installs REDCap deploys hooks exclusively from the REDCap-Extras repository:
[REDCap Extras](https://github.com/ctsit/redcap-extras.git)

These hooks must be deployed into the REDCap instance, and should be selectively
activated. Activations can be global or project specific.

Activation instructions can be found at [Extensible REDCap Hooks](https://github.com/ctsit/redcap-extras/blob/develop/hooks/README.md).

The activated hook list for the CTSI production instance is in the folder /hooks/redcap.ctsi.ufl.edu

The activated hook list for the CTSI staging instance is in the folder /hooks/redcapstage.ctsi.ufl.edu

The hooks library is deployed to the folder $REDCAP_ROOT/hooks/library

The main REDCap hook function is deployed to $REDCAP_ROOT/hooks/redcap_hooks.php

Global REDCap hooks are sym linked from the library to $REDCAP_ROOT/hooks/$HOOKNAME/scriptname.php

Project specific hooks are sym linked from the library to $REDCAP_ROOT/hooks/pid$project_id/$HOOKNAME/scriptname.php