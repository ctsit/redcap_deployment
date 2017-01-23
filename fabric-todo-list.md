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
* DONE apply_patches - modify the apply_patches function prototype to locally run the commands it currently prints
* DONE configure_redcap_cron - see redcap\_deployment\_functions.sh
* DONE move_edocs_folder - see redcap\_deployment\_functions.sh
* DONE set_hook_functions_file - see redcap\_deployment\_functions.sh
* DONE Remove upload_package - we no longer need it.  IT has bene replaced by make_upload_target and upload_package_and_extract
* Make required directories for hook deployment - deployment_functions.sh
* Create sym links for hooks to be executed - deployment_functions.sh

## deploy function

DONE deploy(name) - Revise the existing deploy function to call the functions needed to do a deployment of a new instance.  These packages are probably need in this order:

    make_upload_target()
    upload_package_and_extract(name)
    update_redcap_connection()
    write_remote_my_cnf()
    create_redcap_tables()
    move_edocs_folder()
    set_redcap_base_url()
    set_hook_functions_file()
    configure_redcap_cron()

In a normal workflow, `deploy` might be preceeded by `create_database`

At the same time delete these functions as they will no longer be referenced by deploy

    git_version(version)
    package_files()
    ship_to_host()
    create_backup()
    unpackage_files()
    link_to_live()
    refresh_server()
    clean_up()


## Things fabric must do to upgrade an existing instance
* upgrade - a function to upgrade an existing redcap. This function would call:
    * DONE make_upload_target
    * DONE copy_running_code_to_backup_dir
    * DONE upload_package_and_extract - to deploy package to remote (upload package needs to be split into make_upload_target and upload_package_and_extract so copy_running_code_to_backup_dir can be spliced in before extract)
    * DONE offline - use set_redcap_config to go offline
    * DONE move_software_to_live - replace symbolic link to old code with symlink to new code.
    * apply_upgrade_sql - make a function that tests for the existence of the file upgrade.sql in the root of the redcap app, applies upgrade.sql the redcap database if it does exist and then deletes upgrade.sql on success.
    * DONT DO fix_shibboleth_exceptions - we will do this manually (we really need to obsolete this with ideas from the redcap forum)
    * DONE online - use set_redcap_config to go online


## Things we would like Fabric to do but might delay

* DONE backup mysql database from the remote host
* make_twilio_features_visible - see redcap\_deployment\_functions.sh
* Read remote database.php to get credentials for DB operations.
* apply_incremental_db_changes - remotely execute the multiple version.sql files during an upgrade


