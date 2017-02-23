# Deploying a REDCap package for deployment

This guide will provide the sequence of fabric commands needed to *deploy* a packaged version of REDCap. See the REDCap Deployment Tools document (redcap_deployment_commands_documentation.md) for more details about the individual commands.

---

### Prerequisites  
Deployment requires an existing REDCap package in the format created by `fab package(redcap_zip)` (redcap-#.#.#.tgz). Note an instance (or deployment environment) must be specified in order to establish necessary configuration parameters.

## Fabric Command Sequence
The command to run is `fab [instance] deploy(package_name,force)`. The [instance] is the desired environment such as vagrant, staging, or prod (for dev testing, further testing, and live deployment, respectively). The package_name is the name to the tgz file you want to deploy - in the format of redcap-#.#.#.tgz. The last parameter, force, takes an affirmative (true, yes, y, etc.) or negative (anything else) argument. If affirmative, redcap cron deployment is executed, if negative (anything not affirmative) redcap cron is not deployed.  

The deploy command does the following:  
* Creates a backup directory with the format of [backup_prepath]/redcap-[datetime]/ (for example - /var/www.backup/redcap-20170221T0831/). Unzips the contents of the package and copies/synchronizes the contents to the backup directory. Then the database settings are specified based on the instance chosen. An empty database is created if the deployment instance is vagrant. The database permissions are granted to deploy_user. The redcap tables are created up to the appropriate tables associated with the package version. Backup all existing files and then switch the symlink to the existing files. Then edocs are copied to the remote and removed from the live symlink to keep them secure from web access. The redcap url is set in the redcap config table. The hook functions file is also set in the redcap config table. The redcap cron is configured if forced or if in the vagrant instance. Finally, tests are run and then the remote cnf file is removed.