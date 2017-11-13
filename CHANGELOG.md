# Change Log
All notable changes to the REDCap Deployment project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).


## [1.3.0] - 2017-11-13
## Added
- Add support for External Modules. (Tiago Bember Simeao)
- Add support for installing External Modules
- Add enable/disable module methods for redcap (marlycormar)
- Provide example modules.json config file for module installation

## Changed
- Upgrade development environment to PHP7 (marlycormar, tbembersimeao)
- Grant access to DATABASE_USER@% so the VM host can access mysql on port 3306 (Philip Chase)
- Fixing composer installation. (Tiago Bember Simeao)
- Fix issue in test.py where the conditionals where not set properly (marlycormar)
- Modify enable/disable methods to use existing php methods instead of directly updating the db (marlycormar)
- Moving Composer dependencies installation to the packaging step. (Tiago Bember Simeao)
- Fix plugin test by running scripts as user deploy (marlycormar)
- Fix hook activation by running certain scripts as user deploy (marlycormar)
- Handling different REDCap version's ways to set up hooks. (Tiago Bember Simeao)


## [1.2.0] - 2017-08-15
### Added
- Add new users and change passwords to 'password' in test_with_table_based_authentication.sql (Philip Chase)
- Add scripts to deploy `ssl.conf` (marlycormar)
- Add `ssl.conf` file containing the required cipher suites to comply with the NIST document on server security (marlycormar)
- Add pdf toolkit installation to the provisioning scripts (marlycormar)
- Add a SQL file that can be used to fix busted PRMIS credentials (Philip Chase)
- Add script to disable Messenger (marlycormar)
- Add deployment of linear work flow deploy script (suryayalla)
- Add deployment of find_survey_from_survey_hash plugin (Stewart Wehmeyer)
- Add deployment of custom_project_settings_plugin (suryayalla)
- Add test methods testSendItDownload and testRouteToSendItController (Philip Chase)
- Add option to follow redirects in tests (Philip Chase)

### Changed
- Remove lines that were changing env.user to deploy_user (Philip Chase)
- Fix PHP 5 installation by using oldstable debian repos as sources. (Tiago Bember Simeao)
- Import configparser from six.moves to address fabric import failures when fabric is installed using brew (suryayalla)


## [1.1.0] - 2017-05-31
### Added
- Add documentation for language configuration (marlycormar)
- Modify deploy_language_to_build_space function to allow either a list or a folder as a language configuration (marlycormar)

### Changed
- Don't load any database upgrade scripts with a version number higher than the version you are upgrading to (Philip Chase)

## [1.0.2] - 2017-05-25
### Added
- Add DOI to README (Philip Chase)

### Removed
- Remove the Condensed PDF Plugin because it is buggy and we have no funds to rewrite it (Philip Chase)

### Changed
- Revise instructions in prompt_to_install.md (Stewart Wehmeyer)


## [1.0.1] - 2017-05-19
### Added
- Add DOI to README (Philip Chase)


## [1.0.0] - 2017-05-19
### Changed
- Replace Vagrant-based REDCap deployment with Fabric-based deployment (Philip Chase)
- Clean up files on the root of the project (Philip Chase)
- Add test_plugin task to fabfile to test a plugin under development in the host OS (Philip Chase)
- Moved settings/*.ini files to *.example

### Added
- Add Authors file (Philip Chase)

### Removed
- Remove old hooks, plugins, and config files (Philip Chase)


## [0.9.1] - 2017-04-21
### Added
- Specify fields written in test_with_table_based_authentication.sql to support a broader range of REDCap versions including 7.2.x (Philip Chase)
- Update project description in README (Philip Chase)
- Switch extensible-redcap-hooks back to production repo (Philip Chase)
- Add deployment script for modify_contact_admin_button (Philip Chase)


## [0.9.0] - 2017-03-17
### Added
- Add the hook.py module with activate and test methods (Stewart Wehmeyer, Philip Chase)

### Changed
- Configure apache to follow symbolic links to simplify use and testing of hook framework (Philip Chase)
- Switch hook framework to a different fork, https://github.com/pbchase/extensible-redcap-hooks.git (Philip Chase)


## [0.8.1] - 2017-03-17
### Added
- Add documentation about the fabric tools in README.md and ./docs/ (Stewart Wehmeyer, Philip Chase)

### Changed
- Refactor upgrade, deployment, packaging and utility and utility_redcap tasks into their own modules (Sreeja)
- Make the /vagrant folder in the VM accessible to the web server (Philip Chase)
- Change source repo for redcap-custom-dashboard (Philip Chase)
- Make redcap temp space writeable in upload_package_and_extract (Philip Chase)
- Turn deploy_redcap_cron into a boolean to assure cron will not inadvertently deploy (Philip Chase)


## [0.8.0] - 2017-02-13
### Added
- Add support for configurable language module deployment (Philip Chase)
- Add redcap-custom-dashboard plugin (Philip Chase)

### Changed
- Add state for write_remote_my_cnf and delete_remote_my_cnf functions (Sreeja Kannagundla)
- Write the instance name into the backup file name in backup_database (Philip Chase)
- Run tests from fabric during upgrade, deploy and as a standalone method (Philip Chase, Sreeja Kannagundla)
- Compress database backups to reduce storage and write time (Philip Chase)
- Require a configuration switch to deploy REDCap cron (Philip Chase)
- Look for 'Create New Project' in testRedcapRootFolder to determine if we are logged in (Philip Chase)


## [0.7.0] - 2017-02-02
### Added
- Packaging, deployment, upgrade and backup tools based on the Python Fabric API (Sreeja KannaGundla, Stewart Wehmeyer, Philip Chase)
- Deployed REDCap Instance testing based on PyUnit (Philip Chase)
- Add Expected Upgrade Workflow (Philip Chase)

### Changed
- Update README for focus on packaged deployment (Philip Chase)


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
