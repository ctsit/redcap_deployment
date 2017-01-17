# Things Fabric must do to provide the functionality we need for REDCap packaging and deployment

## Things Fabric must do to package REDCap

* DONE make temporary builddir
* DONE locate redcap\<version\>.zip
* DONE extract redcap\<version\>.zip into builddir
* DONE Using git_version - checkout named commits
* copy named components from redcap_deployment into build space
* DONE deploy_plugins_in_build_space execute all deploy.sh scripts in ./deploy/plugins/*/deploy.sh
* DONE deploy_hooks_into_build_space execute all deploy.sh scripts in ./deploy/hooks/*/deploy.sh
* DONE package_redcap - make a timestamped TGZ of the entire content of the builddir. Use git workdir contents if version is not specified


## Things Fabric must do to deploy REDCap

* DONE Deploy code into a time-stamped "backup" directory
* DONE Upload package
* DONE Extract package
* DONE create_table - (re)create the empty database that is to hold the REDCap DB
* DONE update_redcap_connection_settings - update database.php with database settings
* DONE set_redcap_config - see redcap\_deployment\_functions.sh
* DONE configure_redcap - see redcap\_deployment\_functions.sh
* DONE create_redcap_tables - see redcap\_deployment\_functions.sh
* DONE configure_redcap - see redcap\_deployment\_functions.sh
* apply_patches - Apply patches to REDCap
* DONE configure_redcap_cron - see redcap\_deployment\_functions.sh
* move_edocs_folder - see redcap\_deployment\_functions.sh
* DONE set_hook_functions_file - see redcap\_deployment\_functions.sh
* Make required directories for hook deployment - deployment_functions.sh
* Create sym links for hooks to be executed - deployment_functions.sh


## Things fabric must do to upgrade an existing instance
* upgrade - a function to upgrade an existing redcap. This function would call:
    * DONE make_upload_target
    * copy_running_code_to_backup_dir
    * upload_package_and_extract - to deploy package to remote (upload package needs to be split into make_upload_target and upload_package_and_extract so copy_running_code_to_backup_dir can be spliced in before extract)
    * offline - use set_redcap_config to go offline
    * move_software_to_live - replace symbolic link to old code with symlink to new code.
    * upgrade_db - will do this manually at first
    * fix_shibboleth_exceptions - we will do this manually (we really need to obsolete this with ideas from the redcap forum)
    * online - use set_redcap_config to go online


## Things we would like Fabric to do but might delay

* DONE backup mysql database from the remote host
* make_twilio_features_visible - see redcap\_deployment\_functions.sh
* Read remote database.php to get credentials for DB operations.
* offline - Take REDCap offline.
* generate upgrade.sql - This will be harder as we will need to copy RC code to make our own PHP-based command line tools generate the upgrade.sql.
* upgrade_db - execute upgrade.sql - pending the generation of upgrade.sql
* online - Put REDCap online.

