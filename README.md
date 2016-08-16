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

This VM requires that Vagrant, VirtualBox, the vagrant-hostsupdater plugin and
the vagrant-env plugin be installed on the host system.


### Install Vagrant and Virtual Box

On a Linux machine run these commands in a shell:

    sudo apt-get install vagrant
    sudo apt-get install virtualbox

On a Mac OSX machine:

-   Download and install vagrant from <https://www.vagrantup.com/downloads.html>
-   Download and install the latest virtual box from <http://download.virtualbox.org/virtualbox/>

On Mac OSX users using [Homebrew](http://brew.sh/) can install these packages
using the _brew_ command.  Run these commands at a shell:

    brew install virtualbox
    brew install vagrant


### Install Vagrant plugins

Vagrant will need a few plugins for this VM. On any platform, run these commands in a shell:

    vagrant plugin install vagrant-hostsupdater
    vagrant plugin install vagrant-env

Mac OSX users might enjoy the functionality of the vagrant-triggers plugin.  CTS-IT used it to open the Chrome browser to the just -deployed REDCap instance. Run this command at a shell to install it.

    vagrant plugin install vagrant-triggers

For more details about Vagrant software you can go to [why-vagrant](https://docs.vagrantup.com/v2/why-vagrant/) page.


### Get your REDCap zip file

You must provide a copy of the REDCap software from http ://project-redcap.org/. Save the .zip file with its default name to the root of this repository. This ensures the provisioning script [bootstrap.sh](bootstrap.sh) script can extract the files to the virtual machine path "**/var/www/redcap**".

If you put multiple redcap\*.zip files in the root folder, the provisioning script will use the one with the highest version number.


## Configure the Development Environment

The development environment needs to be configured before it can be started.
Copy the file _example.env.txt_ to the name _.env_ and customize it for your
use. Minimally, you will need to set _smtp\_smarthost_ to the dns name of a mail
server your development host can use to deliver mail.  This will allow you to
better test features that send email.


## Using the Development Environment

With the above requirements and configuration completed, start the VM with the command

    vagrant up

After about two minutes, the VM should be accessible at [http://redcap.dev/redcap/](http://redcap.dev/redcap/) and at [https://redcap.dev/redcap/](https://redcap.dev/redcap/) (or whatever URL _URL\_OF\_DEPLOYED\_APP_ is set to in _.env_)


## Hook and Plugin Deployment

CTSI REDCap Hooks and Plugins are deployed using the script
deploy_extensions.sh in this repo.  This repo also contains the data files
need to configure hook deployment for the CTSI REDCap instances.  See [Hook
Deployment ](README-hooks.md) for usage instructions and details.


## REDCap Upgrade

At the moment, CTS-IT does not have a fully scripted upgrade or procedures
that can be be shared publicly.  The upgrade procedures used live in a private
Wiki article found at [CTS-IT Wiki Article on REDCap Upgrades](https://ctsit-
forge.ctsi.ufl.edu/projects/redcap/wiki/REDCap_Upgrade_Instructions)

ToDo: Move wiki article to a markdown doc in this repo.
ToDo: Convert steps of wiki article to shell script.


## REDCap Installation

CTS-IT does not currently have a bare-metal installation procedure. That said, the
vagrant files presented in this repo contain many of the required steps in
such a deployment process.

ToDo: Make vagrant provisioning scripts more like a production deployment.


## Contributions

This repository was created to meet the needs of the UF CTSI REDCap Team.  We
have shared it as an example of how scripted deployments can be done in a
Debian Linux environment.  We welcome contributions that parameterize our work
to make these scripts more accessible to other REDCap sites.  Please fork this
repository to commit and share your work.  Please make pull requests against
the develop branch of this repo if you would like to make a contribution.
