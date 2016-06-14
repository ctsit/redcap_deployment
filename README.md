# REDCap Deployment Scripts

## Overview

This repo documents the scripts and tools used by CTS-IT for deployments and
upgrades to the CTSI REDCap staging and production instances. This repo
includes a Vagrant VM on which these tools can be developed and tested.

This repo also contains the mapping of hooks to specific project id's for the
production and staging instances of REDCap at the CTSI.


## Requirements

A user of these tools will need to download and provide their own REDCap zip file,
downloaded from Vanderbilt. This REDCap .zip should be placed in the root folder.
It should not be renamed.

This VM requires that Vagrant, VirtualBox, the vagrant-hostsupdater plugin and the vagrant-env plugin be installed on the host system.

See [Creating the Test VM With Vagrant](docs/creating_the_test_vm_with_vagrant.rst) for details on how to meet those requirements.


## Configure the Development Environment

The development environment needs to be configured before it can be started.
Copy the file _example.env.txt_ to the name _.env_ and customize it for your
use. Minimally, you will need to set _smtp\_smarthost_ the dns name of a mail
server your development host can use to deliver mail.  This will allow you to
better test features that send email.

## Using the Development Environment

With the above requirements and configuration completed, start the VM with the command

    vagrant up

After about two minutes, the VM should be accessible at [http://redcap.dev/redcap/](http://redcap.dev/redcap/) and at [https://redcap.dev/redcap/](https://redcap.dev/redcap/) (or whatever URL _URL\_OF\_DEPLOYED\_APP_ is set to in _.env_)


## Hook and Plugin deployment

CTSI REDCap Hooks and Plugins are deployed using the script
deploy_extensions.sh in this repo.  This repo also contains the data files
need to configure hook deployment for the CTSI REDCap instances.  See [Hook
Deployment ](README-hooks.md) for usage instructions and details.


## REDCap upgrade

Upgrade instructions currently live in a Wiki article found at
[CTS-IT Wiki Article on REDCap Upgrades](https://ctsit-forge.ctsi.ufl.edu/projects/redcap/wiki/REDCap_Upgrade_Instructions)

ToDo: Move wiki article to a markdown doc in this repo.
ToDo: Convert steps of wiki article to shell script.


## REDCap installation

CTS-IT does not currently have a bare-metal installation procedure. That said, the
vagrant files presented in this repo contain many of the required steps in
such a deployment process. Other steps can be found in the above upgrade
instructions.

ToDo: Make vagrant provisioning scripts more like a production deployment, but
don't be too wed to the prod and stage instance we have today.  Make the
deployment we _want_, not the deployment we have.


## Contributions

This repository was created to meet the needs of the UF CTSI REDCap Team.  We
have shared it as an example of how scripted deployments can be done in a
Debian Linux environment.  We welcome contributions that parameterize our work
to make these scripts more accessible to other REDCap sites.  Please fork this
repository to commit and share your work.  Please make pull requests against
the develop branch of this repo if you would like to make a contribution.
