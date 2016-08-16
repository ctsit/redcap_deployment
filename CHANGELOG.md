# Change Log
All notable changes to the REDCap Deployment project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [0.6.1] - 2016-08-15
### Changed
- Replace patching of default-ssl.conf with warning if there is no line to include ssl-includes/ (Philip Chase)
- Fix typos in the README (Philip Chase)

## [0.6.0] - 2016-08-01
### Changed
- Merge Requirements section from docs/creating_the_test_vm_with_vagrant.rst into README and update text of README (Philip Chase)

### Added
- Add condensed_pdf_report plugin (Philip Chase)


## [0.5.0] - 2016-06-14
### Changed
- Refactor dev VM and its related deployment scripts to use the vagrant-env plugin, Debian Jessie, and MySQL Community Server (Philip Chase)
- Fix formatting errors in 'Creating the Test VM With Vagrant' and embellish content (Philip Chase)
- Use our apache ssl configuration (Philip Chase)
- Check for box file updates at 'vagrant up' (Philip Chase)
- Reconfigure how the autonotify plugin deployment integrates with apache (Philip Chase)


## [0.4.1] - 2016-04-25
### Changed
- Correct documentation and make it more suitable for public consumption (Philip Chase)


## [0.4.0] - 2016-04-25
### Added
- Enable ssl in apache config (Philip Chase)
- Add an alias, dump_redcap_db, to do a standardized dump of the REDCap MySQL DB (Philip Chase)
- Add set_redcap_config for updating the redcap_config table (Philip Chase)

### Changed
- Disable stream edits of the SHIB configuration in a test environment (Philip Chase)
- Set hook_functions_file to the path used in deployment_functions.sh (Philip Chase)
- Configure REDCap VM according to recommendations: install php-gd, activate redcap cron, adjust php ini vars, and move edocs folder (Philip Chase)
- Fix patching of default-ssl in autonotify plugin deploy script. (Philip Chase)


## [0.3.0] - 2016-04-01
### Changed
- Update autonotify plugin with security improvements (Philip Chase)


## [0.2.0] - 2016-03-31
### Added
- Add a Changelog with retrospective releases (Philip Chase)
- Add scripts for deploying REDCAP Plugins from this Repo (Philip Chase)
- Add Autonotify_Plugin_End_User_Instructions.docx (Philip Chase)
- Add REDCAp Autonotify Plugin from Andy Martin (Philip Chase)

### Changed
- Refactor hook deployment script to allow for deploying other extensions (Philip Chase)
- Move Vagrant VM to a debian-7.8 image (Philip Chase)
- Reconfigure Vagrant to deploy REDCap extensions entirely via shell provisioning (Philip Chase)
- Configure redcap to use the redcap.dev hostname in redcap_base_url (Philip Chase)
- Move vagrant config to the root of the repo (Philip Chase)


## [0.1.0] - 2015-07-02
### Added
- Add REDCAP hook deployment script and sample data file (Erik C. Schmidt)
- Add vagrant testing VM
- Add a hooks data file for redcap.ctsi.ufl.edu (Philip Chase)
- Add a hooks data file for redcapstage.ctsi.ufl.edu (Philip Chase)
