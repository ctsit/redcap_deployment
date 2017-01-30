# Things Fabric must do to provide the functionality we need for REDCap packaging, deployment, and upgrade.


## Things fabric must do before we can use it on staging and prod

* DONE apply_incremental_db_changes still needs:
    * DONE a function to tell it the currently installed verison of redcap.  Read the redcap_config table to get it. Call this funciton to get 'old'
    * DONE a function to tell it the version number of the package being deployed.  Perhaps this is already in a variable?  This value will be supplied for 'new'
    *DONE silence the massive list of .sql and .php files echoed to the screen during the ls.  It is very distracting.
* DONE Change the functions listed here to run as the 'deploy' user. i.e. prefix the 'run' and 'put' commands with 'with settings(user=env.deploy_user):'
    * write_remote_my_cnf
    * backup_database
    * update_redcap_connection
    * create_database
    * set_redcap_config
    * create_redcap_tables
    * apply_upgrade_sql
    * apply_incremental_db_changes
* DONE In 'configure_redcap_cron', '/etc/cron.d/redcap' should be '/etc/cron.d/%s' % env.project_name to better support multiple instances on a single host.
* Make 'stage' load settings/stage.ini much like 'vagrant' loads vagrant.ini
* Make 'prod'  load settings/prod.ini  much like 'vagrant' loads vagrant.ini
* Address the problem of 'deploy' requiring sudo perms in 'configure_redcap_cron'.


## Things Philip must do

* Write settings/stage.ini
* Write settings/prod.ini


## Things we should do soon:

* Improve the first doc string so 'fab --list' is *very* helpful.
* Write a markdown file describing the fab tools and how they should be used for development, packaging, and deployments.
* Replace the bootstrap.sh redcap deployment with fabric packaging and deployment and remove the related dead code.
* Add the new and updated plugins for our customers.
* Write a function "delete_remote_my_cnf" that deletes ~/.my.cnf on the remote host. See write_remote_my_cnf for reference.
* Call 'delete_remote_my_cnf' as the final step in both 'upgrade' and 'deploy'
* move apply_patches into the correct sequence amongst the packaging functions
* move add_db_upgrade_script into the correct sequence amongst the packaging functions


## Things we would like Fabric to do but might delay

* make_twilio_features_visible - see redcap\_deployment\_functions.sh
* Read remote database.php to get credentials for DB operations.
* Make required directories for hook deployment - deployment_functions.sh
* Create sym links for hooks to be executed - deployment_functions.sh
* move '    sudo("mkdir -p %s" % env.edoc_path)' out of setup webspace as it is too specific to redcap.  Maybe it should be addressed with 'configure_redcap_cron' as they both REDCap deployment tasks that require sudo permissions.
* Write a fab function to run the tests against a particular instance.
* Run tests at end of 'deploy'.
* Run tests at end of upgrade just before 'online'.
