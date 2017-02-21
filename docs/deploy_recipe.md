# Deploying a REDCap package for deployment

This guide will provide the sequence of fabric commands needed to *deploy* a packaged version of REDCap. See the REDCap Deployment Tools document (redcap_deployment_commands_documentation.md) for more details about the individual commands.

---

### Prerequisites  
Deployment requires an existing REDCap package in the format created by `fab package(redcap_zip)` (redcap-#.#.#.tgz). Note an instance (or deployment environment) must be specified in order to establish necessary configuration parameters.

## Fabric Command Sequence
The command to run is `fab [instance] deploy(package_name,force)`. The [instance] is the desired environment such as vagrant, staging, or prod (for dev testing, further testing, and live deployment, respectively). The package_name is the name to the tgz file you want to deploy - in the format of redcap-#.#.#.tgz. The last parameter, force, takes an affirmative (true, yes, y, etc.) or negative (anything else) argument. If affirmative, redcap cron deployment is executed, if negative (anything not affirmative) redcap cron is not deployed.  

The deploy command does the following:  
* Creates a backup dir with the format of [backup_prepath]/redcap-[datetime]/ (for example - /var/www.backup/redcap-20170221T0831/). 

@task
def deploy(name,force=""):
    """
    Deploy a new REDCap instance defined by <package_name>, optionally forcing redcap cron deployment

    """
    make_upload_target()
    upload_package_and_extract(name)
    update_redcap_connection()
    write_remote_my_cnf()
    if env.vagrant_instance:
        create_database()
    create_redcap_tables()
    move_software_to_live()
    move_edocs_folder()
    set_redcap_base_url()
    set_hook_functions_file()
    force_deployment_of_redcap_cron = is_affirmative(force)
    configure_redcap_cron(env.deploy_redcap_cron, force_deployment_of_redcap_cron)
    test()
    delete_remote_my_cnf()
    #TODO: Run tests