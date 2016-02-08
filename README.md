# REDCap Deployment Scripts

## Overview

This repo documents the scripts and tools used by CTS-IT for  deployments and
upgrades to the CTSI REDCap staging and production instances. This repo
includes a Vagrant VM on which these tools can be developed and tested.

This repo also contains the mapping of hooks to specific project id's for the
production and staging instances of REDCap at the CTSI.


## Requirements

A user of these tools will need to download and provide their own REDCap bits,
downloaded from Vanderbilt. This REDCap .zip should be placed in the /vagrant folder.
It should not be renamed.

This VM requires that Vagrant and VirtualBox be installed on the host system.


## REDCap upgrade

Upgrade instructions currently live in a Wiki article found at
[CTS-IT Wiki Article on REDCap Upgrades](https://ctsit-forge.ctsi.ufl.edu/projects/redcap/wiki/REDCap_Upgrade_Instructions)

ToDo: Move wiki article to a markdown doc in this repo.
ToDo: Convert steps of wiki article to shell script.


## REDCap installation

We do not currently have a bare-metal installation procedure. That said, the
vagrant files presented in this repo contain many of the required steps in a
deployment process. Other steps can be found in the above upgrade
instructions.

ToDo: Make vagrant provisioning scripts more like a production deployment, but
don't be too wed to the prod and stage instance we have today.  Make the
deployment we _want_, not the deployment we have.


## Hook deployment

CTSI REDCap Hooks are deployed using the script redcap_hooks.sh from this
repo, ssh://git@ctsit-forge.ctsi.ufl.edu/redcap_deployment.git.  This repo
also contains data files for CTSI REDCap Instance.  See [Hook Deployment
](README-hooks.md) for usage instructions and details.
