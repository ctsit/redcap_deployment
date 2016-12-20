# REDCap Deployment Scripts

## Overview

This project provides tools for scripted deployments of REDCap instances and the extensions installed within them. The tools achieve this through scripted building of packages of the REDCap with extensions and scripted deployment of those packages to hosts. The goal of the project is to build packages rapidly and consistently across REDCap version numbers and deployed instances. This will reduce the cost of testing, the variability in test environments, and the costs of upgrading REDCap instances.

Ancillary to this goal, this project provides a local REDCap instance that can be used as an educational REDCap tool and/or a software development test bed. You can use this project for any or all of these goals.


## Requirements

### REDCap

A user of these tools will need to download and provide their own REDCap zip
file, downloaded from Vanderbilt. This REDCap .zip should be placed in the
root folder of this project. It should not be renamed.

### Virtual Machine

This project provides a virtual machine wherein it hosts the local REDCap instance. Creating the virtual machine (VM) the software packages Vagrant, VirtualBox, the vagrant-hostsupdater plugin and the vagrant-env plugin be installed on the host system.

### Packaging and Deployment

The packaging and deployment tools are designed to deploy REDCap to Debian Linux hosts. They may or may not work with non-Debian REDCap hosts and cannot deploy REDCap to Windows hosts. The packaging and deployment tools written using the [Fabric](http://www.fabfile.org/) system. Fabric is written in Python, so both Python 2.7 and Fabric must be installed to do packaging and deployment.


## Installing dependencies

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

You must provide a copy of the REDCap software from https://projectredcap.org/. Save the .zip file with its default name to the root of this repository. This ensures the packaging and provisioning scripts can locate the REDCap code when needed.

If you put multiple redcap\*.zip files in the root folder, the provisioning script will default to using the one with the highest version number.


## Configure the Virtual Machine

The development environment needs to be configured before it can be started.
Copy the file _example.env.txt_ to the name _.env_ and customize it for your
use. Minimally, you will need to set _smtp\_smarthost_ to the dns name of a mail
server your development host can use to deliver mail.  This will allow you to
better test features that send email.


## Using the testing and development environment

With the above requirements and configuration completed, start the VM with the command

    vagrant up

After about two minutes, the VM should be accessible at the value you set for _URL\_OF\_DEPLOYED\_APP_ is set to in _.env_  By default this is [http://redcap.dev/redcap/](http://redcap.dev/redcap/)


## Hook and Plugin Deployment

The VM provisioning scripts will automatically deploy all hooks and plugins described in the sub directories of ./deploy/hooks, ./deploy/hook-framework, and ./deploy/plugins as long as those extensions comply with the specification defined in ./docs/redcap_extension_deployment_specification.md


## Hook and Plugin Development

The directories of deployed hooks and plugins are accessible from the host computer in this project directory at ./redcap/hooks and ./redcap/plugins.  Indeed, the entire deployed REDCap code base is accessible.  This allows the deployed code base to be modified on the fly. Use the aid development and expermentation, but beware that these files will be erased if you destroy the VM.


## Contributions

This repository was created to meet the needs of the UF CTSI REDCap Team.  We
have shared it as an example of how scripted deployments can be done in a
Debian Linux environment.  We welcome contributions that parameterize our work
to make these scripts more accessible to other REDCap sites.  Please fork this
repository to commit and share your work.  Please make pull requests against
the develop branch of this repo if you would like to make a contribution.
