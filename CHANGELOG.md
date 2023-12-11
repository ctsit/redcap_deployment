# Change Log
All notable changes to the REDCap Deployment project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [3.2.0] - 2023-12-11
### Added
- Add upgrade_apply_incremental_db_changes_only task (@pbchase)
- Add PHP 7.4-to-8.1 upgrade instructions (@pbchase)
- Add PHP Configuration section to README (@pbchase)
- Add 'Development tools' documentation (@pbchase)
- Add database dump commands for root and vagrant users (@pbchase)

### Changed
- Update post deployment tests (@pbchase)
- Exclude MacOSX's ._* files from the packaged REDCap code (@pbchase)
- Improve docs for installing custom PHP packages (@pbchase)
- Fix BSD tar bug in package.py (@pbchase)
- Replace Fabric3 installation instructions with Fabric 1.x instructions (@pbchase)
- Add commits to /etc during the php upgrade steps (@pbchase)
- Install PHP 7.4, all PHP modules, and composer in README (@pbchase)
- Add code fences, update header depth (@ChemiKyle)
- Suppress warning during mysqldump (@pbchase)
- Set modern permissions on the admin user (@pbchase)
- Update example.env.txt (@mbentz-uf)
- Update CONFIG_VM_BOX to generic/debian (@mbentz-uf)
- Add group write permission to module directory (@mbentz-uf)
- force composer version to 1.x in all scripts where composer is installed needed due to incompatibility with wikimedia/composer-merge-plugin deploy/composer/deploy.sh affects fab instance package (@ChemiKyle)
- update vagrant mysql, 5.6 -> 5.7 required to use redcap_v10.3.0 (@ChemiKyle)
- update gpg servers for mysql (@ChemiKyle)
- recreate the definition of constants from upgrade.php in generate_upgrade_sql_from_php.php (@ChemiKyle)
- use default browser when auto-opening site (@ChemiKyle)
- Add rm_ssh_key task to server_setup.py (@pbchase)
- Make patch deploy scripts executable in package.py (@pbchase)
- relocate and rename vt (@ChemiKyle)
- Removed README references to pycurl after confirming it is not needed (@ChemiKyle)
- pycurl replaced with urllib, BytesIO no longer needed (@ChemiKyle)
- Update for vboxsf fileshare (@ChemiKyle)
- Change sync type to nsf as nsf causes other issues. (Marly Cormar)
- Use nfs to keep shared folder syncronized. (Marly Cormar)
- Update links, wrap commands in blocks, additional osx pycurl help (@ChemiKyle)


## [3.1.0] - 2019-05-14
### Changed
- Change base os to debian stretch in the env file. (Marly Cormar)
- Installing exim4 as some packages are not by default installed. (Marly Cormar)
- Install dirmngr and update the source repos. (Marly Cormar)
- Remove obsolete hooks config. (Marly Cormar)


## [3.0.2] - 2019-04-03
### Changed
- Remove vagrant-triggers installation instructions. (Marly Cormar)
- Use Vagrant's built-in triggers functionality (Philip Chase)
- Update vm to php7.2. (Marly Cormar)


## [3.0.1] - 2018-06-05
### Changed
- Turn off mysql's secure-file-priv in the dev VM (Philip Chase)
- Exclude hook_functions.php from deployment during upgrade processes (Philip Chase)


## [3.0.0] - 2018-06-05
### Changed
- Upgrade to Python3 and Fabric3 (Philip Chase)

### Added
- Provide support for using REDCap's non-upgrade packages during upgrades (Philip Chase)
- Add reference to 'Installing PycURL on macOS High Sierra' for PyCurl help (Philip Chase)
- Add PHP Zip extension and SOAP package in Dev VM. (Tiago Bember Simeao)


## [2.0.2] - 2018-02-15
### Added
- Add .gitattributes file to manage line ending configuration. (Matthew Koch)

### Changed
- Change modules directory permissions (Marly Cormar)
- Update autonotify repo in deploy.sh (Marly Cormar)


## [2.0.1] - 2018-01-31
### Changed
- Rename autonotify3 example file for shib environments (Philip Chase)


## [2.0.0] - 2018-01-28
### Removed
- Remove all support for hook packaging, deployment and activation (Marly)
- Remove plugins that have been replaced by modules (Marly)

### Added
- Add a cron task to deploy.py (Philip Chase)
- Add major version checking before deploying modules framework (Marly)
- Add deployment script and related files for autonotify3 (marlycormar)
- Add deployment script to include go_prod plugin in redcap instance (sreejakann)

### Changed
- Increase PHP's post_max_size and upload_max_filesize to 32mb in Dev VM (Philip Chase)
- Change the domain name of the vagrant VM from redcap.dev to redcap.test (Philip Chase)
- Recurse through REDCap temp space to make even subdirectories writeable (Philip Chase)
- Fixing composer dependencies installation. (Tiago Bember Simeao)


## [1.3.0] - 2017-11-13
### Added
- Add support for External Modules. (Tiago Bember Simeao)
- Add support for installing External Modules
- Add enable/disable module methods for redcap (marlycormar)
- Provide example modules.json config file for module installation

### Changed
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
