# Things Fabric must do to provide the functionality we need for REDCap packaging, deployment, and upgrade.

## Things we should do soon:

* Curate configuration for staging and prod.
* Replace the bootstrap.sh redcap deployment with fabric packaging and deployment and remove the related dead code.


## Things we would like Fabric to do but might delay

* make_twilio_features_visible - see redcap\_deployment\_functions.sh
* Read remote database.php to get credentials for DB operations.
* Make required directories for hook deployment - deployment_functions.sh
* Create sym links for hooks to be executed - deployment_functions.sh
* move '    sudo("mkdir -p %s" % env.edoc_path)' out of setup webspace as it is too specific to redcap.
