# Server setup for a REDCap deployment

This guide will provide the sequence of fabric commands needed to complete *server setup* for REDCap deployment. See the REDCap Deployment Tools document (redcap_deployment_commands_documentation.md) for more details about the individual commands.

---

### Prerequisites  
Because `setup-server` is a command used to prepare packaging and deployment, all that is required is you have the virtual environment (deployment environment) created.

## Fabric Command Sequence  
The command to run is `$ fab [instance] setup_server`. The [instance] is the desired environment such as vagrant, staging, or prod (for dev testing, further testing, and live deployment, respectively).  

This command will create the 'deploy' user and set up the web space (e.g., www) and backup web space (e.g., www.backup). The deploy user will be assigned the appropriate rights for deployment.