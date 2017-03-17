# Upgrade a REDCap instance

This guide will provide the sequence of fabric commands needed to *upgrade* a REDCap deployment. See the REDCap Deployment Tools document (redcap_deployment_commands_documentation.md) for more details about the individual commands.

---

## Prerequisites  
The upgrade process requires that you have a properly running REDCap instance. The version you are upgrading *to* must be greater than or equal to the version to be upgraded. In order to perform an upgrade, you must have packaged (via `fab package`) the upgrade zip file of interest. For example, if you have a vagrant instance of REDCap 6.11.5 and you want to upgrade to 7.2.1 you must use `fab package` on the redcap7.2.1_upgrade.zip before it can be used in the upgrade.  e.g. 

    $ fab package:redcap7.2.1_upgrade.zip

## Fabric Command Sequence for Upgrade
To upgrade and instance use the command `$ fab [instance] upgrade:[name]`. The [instance] is the desired environment such as vagrant, staging, or prod (for dev testing, further testing, and live deployment, respectively). The [name] is the name of the .tgz file you want to use for the upgrade. Continuing the example above, you would execute `$ fab vagrant upgrade:redcap7.2.1_upgrad.tgz`.  

This command will deploy the new code, take the server offline, apply the incremental database upgrades in order, put the server back online, and run a series of smoke tests. If any of the tests fail, the script will take the server offline again. 
