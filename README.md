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

The packaging and deployment tools are designed to deploy REDCap to Debian Linux hosts. They may or may not work with non-Debian REDCap hosts.  They cannot deploy REDCap to Windows hosts. The packaging and deployment tools are written using the [Fabric](http://www.fabfile.org/) system. Fabric is written in Python3, so both Python 3 and Fabric3 must be installed to do packaging and deployment.


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
vagrant plugin install vagrant-vbguest
```

For more details about Vagrant software you can go to [why-vagrant](https://www.vagrantup.com/intro/index.html#why-vagrant-) page.

### Install REDCap Modules
REDCap Deployment supports [REDCap Modules](https://github.com/vanderbilt/redcap-external-modules). In order to deploy external modules, you need to set up `settings/modules.json` file and reference it in your instance's settings.

This project provides an example file, which references a module provided by CTS-IT team. You may copy the file `settings/modules.json.example` to the name `settings/modules.json`, and customize it to your needs.
```bash
cp settings/modules.json.example settings/modules.json
```

Here is how `settings/modules.json` should look like:
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
Copy the file `example.env.txt` to the name `.env` and customize it for your
use. Minimally, you will need to set _smtp\_smarthost_ to the dns name of a mail
server your development host can use to deliver mail.  This will allow you to
better test features that send email.

```bash
cp example.env.txt .env
```


## Using the testing and development environment

With the above requirements and configuration completed, start the VM with the command

```bash
vagrant up
```

The vagrant-hostsupdater plugin will make modifications to your hosts file as the VM starts.  If it prompts you for a password, provide the password you use to login to your computer.

After about two minutes, the VM should be accessible at the value of the variable `URL_OF_DEPLOYED_APP` set in `.env`. By default this is [http://redcap.test/redcap/](http://redcap.test/redcap/)


## (Re)deploying REDCap with Fabric Tools

In addition to the REDCap deployed by the Vagrant provisioning scripts, this repository includes a suite of deployment and upgrade tools that can configure a host for deployment, package REDCap with numerous extensions, deploy a new REDCap instance and upgrade an existing one.  You can use these commands any host where you have sufficient privileges or against this vagrant-deployed VM.

### Fabric Prerequisites

This tool is written in Python 3 and uses Fabric 1.x methods. To use it, make sure you install the latest Fabric 1.x.  See https://www.fabfile.org/installing-1.x.html for details, the TL;DR version is

```bash
pip install 'fabric<2.0'
```


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
fab vagrant package:redcap7.3.0.zip
fab vagrant upgrade:redcap-7.3.0.tgz
```

Note that you do not have to use REDCap's _upgrade_ zip files. The `upgrade` method of the Fabric tools knows to not deploy the few files that would be hazardous to an existing REDCap instance.

If the tests fail and the server is left offline, you can put it back online with

```bash
fab vagrant online
```

## Database errors

Sometimes the upgrade fails in the late stages with a SQL error. When this happens, the system is left offline and the database is in an inconsistent state. You will need to note the error message, review the database upgrade `.SQL` or `.PHP` file it was processing, determine the fault and correct it. Once it is corrected, you will need to re-apply the database changes the upgrade command was trying to apply when it failed and then reapply the rest of the changes. To do that, run the task `upgrade_apply_incremental_db_changes_only`. e.g.

```bash
# This command failed
fab instance:warrior upgrade:redcap-13.11.4.tgz

# ... so now run this
fab instance:warrior upgrade.upgrade_apply_incremental_db_changes_only:redcap-13.11.4.tgz
```

It's a long ugly task name, but it gets the job done. It will assure redcap instance is offline, apply the incremental changes, bump the redcap version, log the upgrade, and bring REDCap back online.


## PHP Configuration

While the deployment scripts in this repo manage the PHP file upload size for the local VM, they do not do the same for a remote host. To do that use commands much like these to increase the upload file size limits

### Upgrade PHP from 7.2 to 7.4

```bash
# Upgrade PHP from 7.2 to 7.4
sudo apt install -y libapache2-mod-php7.4 \
  php7.4 \
  php7.4-cli \
  php7.4-common \
  php7.4-curl \
  php7.4-gd \
  php7.4-imap \
  php7.4-json \
  php7.4-mbstring \
  php7.4-mysql \
  php7.4-odbc \
  php7.4-opcache \
  php7.4-readline \
  php7.4-soap \
  php7.4-xml \
  php7.4-zip

sudo a2dismod php7.2
sudo a2enmod php7.4
sudo systemctl restart apache2

cd /etc
sudo -E git add .
sudo -E git commit -m "Commit PHP upgrades and other files"

cd /etc/php
grep -lr upload_max_filesize * | sudo xargs -i sed "s/upload_max_filesize.*/upload_max_filesize = 256M/;" -i {}
grep -lr post_max_size * | sudo xargs -i sed "s/post_max_size.*/post_max_size = 256M/;" -i {}
grep -lr max_input_vars * | sudo xargs -i sed "s/.*max_input_vars.*/max_input_vars = 100000/;" -i {}
grep -lr session.cookie_secure * | sudo xargs -i sed "s/.*session.cookie_secure.*/session.cookie_secure = On/;" -i {}

cd /etc
sudo -E git add .
sudo -E git commit -m "Commit PHP configuration changes"

# install composer
cd /tmp
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
# safety not guaranteed
# php -r "if (hash_file('sha384', 'composer-setup.php') === '906a84df04cea2aa72f40b5f787e49f22d4c2f19492ac310e8cba5b96ac8b64115ac402c8cd292b8a03482574915d1a8') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
php composer-setup.php
php -r "unlink('composer-setup.php');"
sudo mv composer.phar /usr/local/bin/composer
```

### Upgrade PHP from 7.4 to 8.1

```bash
# Upgrade PHP from 7.4 to 8.0
sudo apt install -y libapache2-mod-php8.1 \
  php8.1 \
  php8.1-cli \
  php8.1-common \
  php8.1-curl \
  php8.1-gd \
  php8.1-imap \
  php8.1-json \
  php8.1-mbstring \
  php8.1-mysql \
  php8.1-odbc \
  php8.1-opcache \
  php8.1-readline \
  php8.1-soap \
  php8.1-xml \
  php8.1-zip

cd /etc
sudo -E git add .
sudo -E git commit -m "Commit PHP upgrades and other files"

cd /etc/php
grep -lr upload_max_filesize * | sudo xargs -i sed "s/upload_max_filesize.*/upload_max_filesize = 256M/;" -i {}
grep -lr post_max_size * | sudo xargs -i sed "s/post_max_size.*/post_max_size = 256M/;" -i {}
grep -lr max_input_vars * | sudo xargs -i sed "s/.*max_input_vars.*/max_input_vars = 100000/;" -i {}
grep -lr session.cookie_secure * | sudo xargs -i sed "s/.*session.cookie_secure.*/session.cookie_secure = On/;" -i {}

cd /etc
sudo -E git add .
sudo -E git commit -m "Commit PHP configuration changes"

# Switch to new PHP in Apache
sudo a2dismod php7.4
sudo a2enmod php8.1
sudo systemctl restart apache2
```

### Install specific PHP packages

On some hosts, you might need to install a specific packages. At UF, we have one host we call "warrior" that needs the `mpdf` package. To install a custom package, first, install `composer`

```sh
# install composer
cd /tmp
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
# safety not guaranteed
# php -r "if (hash_file('sha384', 'composer-setup.php') === '906a84df04cea2aa72f40b5f787e49f22d4c2f19492ac310e8cba5b96ac8b64115ac402c8cd292b8a03482574915d1a8') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
php composer-setup.php
php -r "unlink('composer-setup.php');"
sudo mv composer.phar /usr/local/bin/composer
```

Then run these steps in the current redcap Libraries directory as user deploy

```bash
sudo su - deploy
#cd /var/https/stage_c/redcap_v13.4.11/Libraries/
cd /var/www/prod/redcap_v13.4.11/Libraries/
```

Then run `composer require` with the package you need install:

```sh
composer require mpdf/mpdf:^8
exit
```

Restart apache when you are done

```sh
sudo service apache2 restart
```


## Developer notes

For tips on developing in this environment, see [Development tools](docs/development_tools.md).


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
