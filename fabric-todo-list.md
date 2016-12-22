# Things Fabric must do to provide the functionality we need for REDCap packaging and deployment

## Things Fabric must do to package REDCap

* make temporary builddir
* locate redcap\<version\>.zip
* extract redcap\<version\>.zip into builddir
* checkout named commits of redcap_deployment
* copy named components from redcap_deployment into build space
* execute all deploy.sh scripts in ./deploy/hooks/*/deploy.sh
* execute all deploy.sh scripts in ./deploy/plugins/*/deploy.sh


## Things Fabric must do to deploy REDCap

* Deploy code into a time-stamped "backup" directory
* Upload package
* Extract package
* update_redcap_connection_settings - update database.php with database settings
* create_redcap_tables - see redcap\_deployment\_functions.sh
* configure_redcap - see redcap\_deployment\_functions.sh
* apply_patches - Apply patches to REDCap
* configure_redcap_cron - see redcap\_deployment\_functions.sh
* move_edocs_folder - see redcap\_deployment\_functions.sh
* set_redcap_config - see redcap\_deployment\_functions.sh
* set_hook_functions_file - see redcap\_deployment\_functions.sh
* Make required directories for hook deployment - deployment_functions.sh
* Create sym links for hooks to be executed - deployment_functions.sh

* make_twilio_features_visible - see redcap\_deployment\_functions.sh
* Symlink code in "backup" directory into apache document root location.


## Things we would like Fabric to do but might delay

* Read remote database.php to get credentials for DB operations.
* Take REDCap offline.
* generate upgrade.sql - This will be harder as we will need to copy RC code to make our own PHP-based command line tools generate the upgrade.sql.
* execute upgrade.sql - pending the generation of upgrade.sql
* Put REDCap online.

