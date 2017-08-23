# REDCap Packaging and Deployment Toolset

[![DOI](https://zenodo.org/badge/57070252.svg)](https://zenodo.org/badge/latestdoi/57070252)

## Overview

This project provides tools for scripted deployments and upgrades of REDCap instances and the extensions installed within them. The toolset achieves this through scripted building of packages of the REDCap with extensions as well as the scripted deployment of those packages to hosts. The goal of the project is to provide a tool set that can build packages rapidly and consistently across REDCap version numbers and deploy those packages to new and existing REDCap instances. This reduces the variability between development, testing, and production environments. This in turn reduces the error rates, the cost of testing, and the costs of upgrading REDCap instances.

Ancillary to this goal, this project provides a local REDCap instance that can be used as an educational REDCap tool and/or a software development test bed. You can use this project for any or all of these goals.


## Requirements

### REDCap

A user of these tools will need to download and provide their own REDCap zip
file, downloaded from Vanderbilt. This REDCap .zip should be placed in the
root folder of this project. It should not be renamed.

### Virtual Machine

This project provides a virtual machine wherein it hosts the local REDCap instance. Creating the virtual machine (VM) required the software packages Vagrant, VirtualBox, the vagrant-hostsupdater plugin and the vagrant-env plugin be installed on the host system.

### Packaging and Deployment

The packaging and deployment tools are designed to deploy REDCap to Debian Linux hosts. They may or may not work with non-Debian REDCap hosts.  They cannot deploy REDCap to Windows hosts. The packaging and deployment tools are written using the [Fabric](http://www.fabfile.org/) system. Fabric is written in Python, so both Python 2.7 and Fabric must be installed to do packaging and deployment.


## Installing dependencies

### Install Vagrant and Virtual Box

On a Linux machine run these commands in a shell:

```bash
sudo apt-get install vagrant
sudo apt-get install virtualbox
```

On a Mac OSX machine:

-   Download and install vagrant from <https://www.vagrantup.com/downloads.html>
-   Download and install the latest virtual box from <http://download.virtualbox.org/virtualbox/>

On Mac OSX users using [Homebrew](http://brew.sh/) can install these packages
using the _brew_ command.  Run these commands at a shell:

```bash
brew cask install virtualbox
brew cask install vagrant
```


### Install Vagrant plugins

Vagrant will need a few plugins for this VM. On any platform, run these commands in a shell:

```bash
vagrant plugin install vagrant-hostsupdater
vagrant plugin install vagrant-env
```

Mac OSX users might enjoy the functionality of the vagrant-triggers plugin.  CTS-IT uses it to open the Chrome browser to the root of the web site. Run this command at a shell to install it.

    vagrant plugin install vagrant-triggers

For more details about Vagrant software you can go to [why-vagrant](https://docs.vagrantup.com/v2/why-vagrant/) page.

### Install REDCap Modules
REDCap Deployment supports [REDCap Modules](https://github.com/vanderbilt/redcap-external-modules). In order to deploy external modules, you need to set up `deploy/modules.json` file.

This project provides an example file, which references a module provided by CTS-IT team. You may copy the file `deploy/modules.json.example` to the name `deploy/modules.json`, and customize it to your needs.
```bash
cp deploy/modules.json.example deploy/modules.json
```

Here is how `deploy/modules.json` should look like:
```json
[
    {
        "name": "linear_data_entry_workflow",
        "version": "2.0.0",
        "repo": "https://github.com/ctsit/linear_data_entry_workflow.git",
        "branch": "develop"
    }
]
```


### Get your REDCap zip file

You must provide a copy of the REDCap software from <https://projectredcap.org/>. Save the .zip file with its default name to the root of this repository. This ensures the packaging and provisioning scripts can locate the REDCap code when needed.


## Configure the Virtual Machine

The development environment needs to be configured before it can be started.
Copy the file _example.env.txt_ to the name _.env_ and customize it for your
use. Minimally, you will need to set _smtp\_smarthost_ to the dns name of a mail
server your development host can use to deliver mail.  This will allow you to
better test features that send email.


## Using the testing and development environment

With the above requirements and configuration completed, start the VM with the command

```bash
vagrant up
```

The vagrant-hostsupdater plugin will make modifications to your hosts file as the VM starts.  If it prompts you for a password, provide the password you use to login to your computer.

After about two minutes, the VM should be accessible at the value of the variable _URL\_OF\_DEPLOYED\_APP_ set in _.env_  By default this is [http://redcap.dev/redcap/](http://redcap.dev/redcap/)


## (Re)deploying REDCap with Fabric Tools

In addition to the REDCap deployed by the Vagrant provisioning scripts, this repository includes a suite of deployment and upgrade tools that can configure a host for deployment, package REDCap with numerous extensions, deploy a new REDCap instance and upgrade an existing one.  You can use these commands any host where you have sufficient privileges or against this vagrant-deployed VM.

### Fabric Prerequisites

The Fabric tools require a few python libraries that might not be installed on your computer.  To install them run these commands:

```bash
pip install fabric
pip install configparser
pip install pycurl
pip install cryptography
```

If you have problems install or using these libraries, you might be well-served to setup a Python _virtual environment_. For more information on that see [Virtual Environment Notes](docs/virtual_env_notes.md)


### Configure Fabric for the Virtual Machine

The Fabric tools need to be configured for the Vagrant VM before they can be used.
Copy the file `settings/vagrant.ini.example` to the name `settings/vagrant.ini`, and customize it to your needs.

```bash
cp settings/vagrant.ini.example settings/vagrant.ini
```

Customization is not _required_ but it is useful to add patches and language modules.


### REDCap Deployment

If you have a REDCap zip file, say redcap7.2.2.zip, you can deploy it to the local Vagrant REDCap instance with these commands:

```bash
fab vagrant server_setup
fab vagrant package:redcap7.2.2.zip
fab vagrant delete_all_tables deploy:redcap-7.2.2.tgz
```


### REDCap upgrade

Any upgrade to 7.3.0 would be as simple as

```bash
fab vagrant package:redcap7.3.0_upgrade.zip
fab vagrant upgrade:redcap-7.3.0_upgrade.tgz
```

If the tests fail and the server is offline, you can put it back online with

```bash
fab vagrant online
```

## Language Configuration

REDCap languages can be provided by modifying the _languages_ variable accordingly:
as a json list, e.g., languages = ["Chinese.6.4.3.ini", "German.ini"], or
as a file, i.e., languages = <languageFolder>, in which case the language files *.ini must be located inside the specified folder


## Contributions

This repository was created to meet the needs of the UF CTSI REDCap Team.  We
have shared it as an example of how scripted deployments can be done in a
Debian Linux environment.  We welcome contributions that parameterize our work
to make these scripts more accessible to other REDCap sites.  Please fork this
repository to commit and share your work.  Please make pull requests against
the develop branch of this repo if you would like to make a contribution.
