# Setup server for a REDCap deployment

This guide will provide the sequence of fabric commands needed to complete *server setup* for REDCap deployment. This command uses root-level privileges to prepare a host for deploying software with these Fabric tools. See the REDCap Deployment Tools document (redcap_deployment_commands_documentation.md) for more details about the individual commands.

---

## Prerequisites  
To run this command you will need an account and sudo privileges on the host you wish to configure for deployment. Your account on the host must be configured to use key-based ssh authentication. If you are configuring the vagrant instance, know that the vagrant user already meets these requirements. 

## Fabric Command Sequence for setup_server
The command to run is `$ fab [instance] setup_server`. The [instance] is the desired environment such as vagrant, staging, or prod (for dev testing, further testing, and live deployment, respectively).  

This command will create the 'deploy' user, add your ssh public to the list of authorized keys and set up the web space (e.g., www) and backup web space (e.g., www.backup). The deploy user will be assigned the appropriate permissions and ownership for deployment.

## Adding ssh_keys
This architecture allows an authorized user to add more ssh keys to the list of authorized keys. Given a file `jdoe.pub` that belongs to user `jdoe`, you could authorize John Doe to to deployments with the command

    fab add_ssh_key:jdoe.pub,jdoe
