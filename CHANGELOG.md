# redcap_deployment 3.3.0 (released 2024-12-17)
- Move PHP composer to 2.latest and allow all plugins (@pbchase)
- Update notes about fabric (@pbchase)
- Set timezone in php.ini files (@pbchase)
- Fix PHP8.2 imagick installation (@pbchase)
- Add redcap_redirect to packaged software (@pbchase)
- Add flight tracker host accessibility tests (@ljwoodley, @ChemiKyle, #91, #92)
- Add PHP 8.2 installation code and imagick fixes inspired by the redcapstage debian 12.4 upgrade (@pbchase, #90)
- Add 'Failed SQL upgrades' section to the README (@pbchase, @ChemiKyle, #89)
- Test that version match is not None in apply_incremental_db_changes() (@pbchase)

# redcap_deployment 3.2.1 (released 2023-12-12)
- Make upgrade_apply_incremental_db_changes_only non-default (@pbchase)

# redcap_deployment 3.2.0 (released 2023-12-11)
- Add upgrade_apply_incremental_db_changes_only task (@pbchase)
- Add PHP 7.4-to-8.1 upgrade instructions (@pbchase)
- Add PHP Configuration section to README (@pbchase)
- Add 'Development tools' documentation (@pbchase)
- Add database dump commands for root and vagrant users (@pbchase)
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

# redcap_deployment 3.1.0 (released 2019-05-14)
- Change base os to debian stretch in the env file. (Marly Cormar)
- Installing exim4 as some packages are not by default installed. (Marly Cormar)
- Install dirmngr and update the source repos. (Marly Cormar)
- Remove obsolete hooks config. (Marly Cormar)

# redcap_deployment 3.0.2 (released 2019-04-03)
- Remove vagrant-triggers installation instructions. (Marly Cormar)
- Use Vagrant's built-in triggers functionality (@pbchase)
- Update vm to php7.2. (Marly Cormar)

# redcap_deployment 3.0.1 (released 2018-06-05)
- Turn off mysql's secure-file-priv in the dev VM (@pbchase)
- Exclude hook_functions.php from deployment during upgrade processes (@pbchase)

# redcap_deployment 3.0.0 (released 2018-06-05)
- Upgrade to Python3 and Fabric3 (@pbchase)
- Provide support for using REDCap's non-upgrade packages during upgrades (@pbchase)
- Add reference to 'Installing PycURL on macOS High Sierra' for PyCurl help (@pbchase)
- Add PHP Zip extension and SOAP package in Dev VM. (Tiago Bember Simeao)

# redcap_deployment 2.0.2 (released 2018-02-15)
- Add .gitattributes file to manage line ending configuration. (Matthew Koch)
- Change modules directory permissions (Marly Cormar)
- Update autonotify repo in deploy.sh (Marly Cormar)

# redcap_deployment 2.0.1 (released 2018-01-31)
- Rename autonotify3 example file for shib environments (@pbchase)

# redcap_deployment 2.0.0 (released 2018-01-28)
### Removed
- Remove all support for hook packaging, deployment and activation (Marly)
- Remove plugins that have been replaced by modules (Marly)
- Add a cron task to deploy.py (@pbchase)
- Add major version checking before deploying modules framework (Marly)
- Add deployment script and related files for autonotify3 (marlycormar)
- Add deployment script to include go_prod plugin in redcap instance (sreejakann)
- Increase PHP's post_max_size and upload_max_filesize to 32mb in Dev VM (@pbchase)
- Change the domain name of the vagrant VM from redcap.dev to redcap.test (@pbchase)
- Recurse through REDCap temp space to make even subdirectories writeable (@pbchase)
- Fixing composer dependencies installation. (Tiago Bember Simeao)

# redcap_deployment 1.3.0 (released 2017-11-13)
- Add support for External Modules. (Tiago Bember Simeao)
- Add support for installing External Modules
- Add enable/disable module methods for redcap (marlycormar)
- Provide example modules.json config file for module installation
- Upgrade development environment to PHP7 (marlycormar, tbembersimeao)
- Grant access to DATABASE_USER@% so the VM host can access mysql on port 3306 (@pbchase)
- Fixing composer installation. (Tiago Bember Simeao)
- Fix issue in test.py where the conditionals where not set properly (marlycormar)
- Modify enable/disable methods to use existing php methods instead of directly updating the db (marlycormar)
- Moving Composer dependencies installation to the packaging step. (Tiago Bember Simeao)
- Fix plugin test by running scripts as user deploy (marlycormar)
- Fix hook activation by running certain scripts as user deploy (marlycormar)
- Handling different REDCap version's ways to set up hooks. (Tiago Bember Simeao)

# redcap_deployment 1.2.0 (released 2017-08-15)
- Add new users and change passwords to 'password' in test_with_table_based_authentication.sql (@pbchase)
- Add scripts to deploy `ssl.conf` (marlycormar)
- Add `ssl.conf` file containing the required cipher suites to comply with the NIST document on server security (marlycormar)
- Add pdf toolkit installation to the provisioning scripts (marlycormar)
- Add a SQL file that can be used to fix busted PRMIS credentials (@pbchase)
- Add script to disable Messenger (marlycormar)
- Add deployment of linear work flow deploy script (suryayalla)
- Add deployment of find_survey_from_survey_hash plugin (Stewart Wehmeyer)
- Add deployment of custom_project_settings_plugin (suryayalla)
- Add test methods testSendItDownload and testRouteToSendItController (@pbchase)
- Add option to follow redirects in tests (@pbchase)
- Remove lines that were changing env.user to deploy_user (@pbchase)
- Fix PHP 5 installation by using oldstable debian repos as sources. (Tiago Bember Simeao)
- Import configparser from six.moves to address fabric import failures when fabric is installed using brew (suryayalla)

# redcap_deployment 1.1.0 (released 2017-05-31)
- Add documentation for language configuration (marlycormar)
- Modify deploy_language_to_build_space function to allow either a list or a folder as a language configuration (marlycormar)
- Don't load any database upgrade scripts with a version number higher than the version you are upgrading to (@pbchase)

# redcap_deployment 1.0.2 (released 2017-05-25)
- Add DOI to README (@pbchase)

### Removed
- Remove the Condensed PDF Plugin because it is buggy and we have no funds to rewrite it (@pbchase)
- Revise instructions in prompt_to_install.md (Stewart Wehmeyer)

# redcap_deployment 1.0.1 (released 2017-05-19)
- Add DOI to README (@pbchase)

# redcap_deployment 1.0.0 (released 2017-05-19)
- Replace Vagrant-based REDCap deployment with Fabric-based deployment (@pbchase)
- Clean up files on the root of the project (@pbchase)
- Add test_plugin task to fabfile to test a plugin under development in the host OS (@pbchase)
- Moved settings/*.ini files to *.example
- Add Authors file (@pbchase)

### Removed
- Remove old hooks, plugins, and config files (@pbchase)

# redcap_deployment 0.9.1 (released 2017-04-21)
- Specify fields written in test_with_table_based_authentication.sql to support a broader range of REDCap versions including 7.2.x (@pbchase)
- Update project description in README (@pbchase)
- Switch extensible-redcap-hooks back to production repo (@pbchase)
- Add deployment script for modify_contact_admin_button (@pbchase)

# redcap_deployment 0.9.0 (released 2017-03-17)
- Add the hook.py module with activate and test methods (Stewart Wehmeyer, @pbchase)
- Configure apache to follow symbolic links to simplify use and testing of hook framework (@pbchase)
- Switch hook framework to a different fork, https://github.com/pbchase/extensible-redcap-hooks.git (@pbchase)

# redcap_deployment 0.8.1 (released 2017-03-17)
- Add documentation about the fabric tools in README.md and ./docs/ (Stewart Wehmeyer, @pbchase)
- Refactor upgrade, deployment, packaging and utility and utility_redcap tasks into their own modules (Sreeja)
- Make the /vagrant folder in the VM accessible to the web server (@pbchase)
- Change source repo for redcap-custom-dashboard (@pbchase)
- Make redcap temp space writeable in upload_package_and_extract (@pbchase)
- Turn deploy_redcap_cron into a boolean to assure cron will not inadvertently deploy (@pbchase)

# redcap_deployment 0.8.0 (released 2017-02-13)
- Add support for configurable language module deployment (@pbchase)
- Add redcap-custom-dashboard plugin (@pbchase)
- Add state for write_remote_my_cnf and delete_remote_my_cnf functions (Sreeja Kannagundla)
- Write the instance name into the backup file name in backup_database (@pbchase)
- Run tests from fabric during upgrade, deploy and as a standalone method (@pbchase, Sreeja Kannagundla)
- Compress database backups to reduce storage and write time (@pbchase)
- Require a configuration switch to deploy REDCap cron (@pbchase)
- Look for 'Create New Project' in testRedcapRootFolder to determine if we are logged in (@pbchase)

# redcap_deployment 0.7.0 (released 2017-02-02)
- Packaging, deployment, upgrade and backup tools based on the Python Fabric API (Sreeja KannaGundla, Stewart Wehmeyer, @pbchase)
- Deployed REDCap Instance testing based on PyUnit (@pbchase)
- Add Expected Upgrade Workflow (@pbchase)
- Update README for focus on packaged deployment (@pbchase)

# redcap_deployment 0.6.1 (released 2016-08-15)
- Replace patching of default-ssl.conf with warning if there is no line to include ssl-includes/ (@pbchase)
- Fix typos in the README (@pbchase)

# redcap_deployment 0.6.0 (released 2016-08-01)
- Merge Requirements section from docs/creating_the_test_vm_with_vagrant.rst into README and update text of README (@pbchase)
- Add condensed_pdf_report plugin (@pbchase)

# redcap_deployment 0.5.0 (released 2016-06-14)
- Refactor dev VM and its related deployment scripts to use the vagrant-env plugin, Debian Jessie, and MySQL Community Server (@pbchase)
- Fix formatting errors in 'Creating the Test VM With Vagrant' and embellish content (@pbchase)
- Use our apache ssl configuration (@pbchase)
- Check for box file updates at 'vagrant up' (@pbchase)
- Reconfigure how the autonotify plugin deployment integrates with apache (@pbchase)

# redcap_deployment 0.4.1 (released 2016-04-25)
- Correct documentation and make it more suitable for public consumption (@pbchase)

# redcap_deployment 0.4.0 (released 2016-04-25)
- Enable ssl in apache config (@pbchase)
- Add an alias, dump_redcap_db, to do a standardized dump of the REDCap MySQL DB (@pbchase)
- Add set_redcap_config for updating the redcap_config table (@pbchase)
- Disable stream edits of the SHIB configuration in a test environment (@pbchase)
- Set hook_functions_file to the path used in deployment_functions.sh (@pbchase)
- Configure REDCap VM according to recommendations: install php-gd, activate redcap cron, adjust php ini vars, and move edocs folder (@pbchase)
- Fix patching of default-ssl in autonotify plugin deploy script. (@pbchase)

# redcap_deployment 0.3.0 (released 2016-04-01)
- Update autonotify plugin with security improvements (@pbchase)

# redcap_deployment 0.2.0 (released 2016-03-31)
- Add a Changelog with retrospective releases (@pbchase)
- Add scripts for deploying REDCAP Plugins from this Repo (@pbchase)
- Add Autonotify_Plugin_End_User_Instructions.docx (@pbchase)
- Add REDCAp Autonotify Plugin from Andy Martin (@pbchase)
- Refactor hook deployment script to allow for deploying other extensions (@pbchase)
- Move Vagrant VM to a debian-7.8 image (@pbchase)
- Reconfigure Vagrant to deploy REDCap extensions entirely via shell provisioning (@pbchase)
- Configure redcap to use the redcap.dev hostname in redcap_base_url (@pbchase)
- Move vagrant config to the root of the repo (@pbchase)

# redcap_deployment 0.1.0 (released 2015-07-02)
- Add REDCAP hook deployment script and sample data file (Erik C. Schmidt)
- Add vagrant testing VM
- Add a hooks data file for redcap.ctsi.ufl.edu (@pbchase)
- Add a hooks data file for redcapstage.ctsi.ufl.edu (@pbchase)
