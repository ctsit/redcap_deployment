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

This VM requires that Vagrant and VirtualBox be installed on the host system.

## UPGRADE

Upgrade instructions currently live in a Wiki article found at
[CTS-IT Wiki Article on REDCap Upgrades](https://ctsit-forge.ctsi.ufl.edu/projects/redcap/wiki/REDCap_Upgrade_Instructions)

## INSTALLATION

We do not currently have a bare-metal installation procedure. That said, the vagrant
files presented in this repo contain many of the required steps in a deployment
process. Other steps can be found in the above upgrade instructions.

## HOOK DEPLOYMENT

CTSI REDCap Hooks are deployed using the script redcap_hooks.sh from this repo, ssh://git@ctsit-forge.ctsi.ufl.edu/redcap_deployment.git.  This repo also contains data files for CTSI REDCap Instance.  See [Hook Deployment](README-hooks.md) for usage instructions and details.
