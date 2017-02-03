# Things Fabric must do to provide the functionality we need for REDCap packaging, deployment, and upgrade.

## Things we must do before using this on prod

* Write settings/prod.ini
* Curate configuration for staging and prod.


## Things we should do soon:

* Improve the first doc string so 'fab --list' is *very* helpful.
* Write a markdown file describing the fab tools and how they should be used for development, packaging, and deployments.
* Write a fab function to run the tests against a particular instance.
* Run tests at end of 'deploy'.
* Run tests at end of upgrade just before 'online'.
* Replace the bootstrap.sh redcap deployment with fabric packaging and deployment and remove the related dead code.
* Add the new and updated plugins for our customers.


## Things we would like Fabric to do but might delay

* make_twilio_features_visible - see redcap\_deployment\_functions.sh
* Read remote database.php to get credentials for DB operations.
* Make required directories for hook deployment - deployment_functions.sh
* Create sym links for hooks to be executed - deployment_functions.sh
* move '    sudo("mkdir -p %s" % env.edoc_path)' out of setup webspace as it is too specific to redcap.
