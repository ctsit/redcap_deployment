# Things Fabric must do to provide the functionality we need for REDCap packaging, deployment, and upgrade.

## Things fabric must do to upgrade an existing instance

* apply_incremental_db_changes still needs:
    * a function to tell it the currently installed verison of redcap.  Read the redcap_config table to get it. Call this funciton to get 'old'
    * a function to tell it the version number of the package being deployed.  Perhaps this is already in a variable?  This value will be supplied for 'new'
    * silence the massive list of .sql and .php files echoed to the screen during the ls.  It is very distracting.


## Things we should do soon:

* Improve the first doc string so 'fab --list' is *very* helpful.
* Write a markdown file describing the fab tools and how they should be used for development, packaging, and deployments.
* Replace the bootstrap.sh redcap deployment with fabric packaging and deployment and remove the related dead code.
* Add the new and updated plugins for our customers.


## Things we would like Fabric to do but might delay

* make_twilio_features_visible - see redcap\_deployment\_functions.sh
* Read remote database.php to get credentials for DB operations.
* Make required directories for hook deployment - deployment_functions.sh
* Create sym links for hooks to be executed - deployment_functions.sh
