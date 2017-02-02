# Expected Upgrade Workflow

The packaging and deployment tools in this repository lend themselves to a REDCap upgrade workflow.  That work flow might look something like this:

|Days Budgeted |Role  |Tasks      |
------|---------------|-----------|
|1-2  |Developer      |Develop upgrade package with REDCap code, with extensions, upgrade.sql and deployment script. Test upgrade package. Deploy to staging instance.  |
|2-3  | REDCap Staff  |Test in staging instance using manual validation procedure.  |
|1    | REDCap Staff  |Write upgrade announcement. Set upgrade date. Announce upgrade with at least 7 days notice.  |
|1-2  | REDCap Staff  |Write documents for describing new features.  |
|1-2  | REDCap Staff  |If needed, update manual validation procedure.  |
|1    |Systems / REDCap Staff  |Deploy to production instance. Test production instance. If tests fail, rollback prod. instance.  |


## Roles

The work of REDCap upgrade and deployment using these tools requires a broad
set of skills including Linux systems administration, MySQL database
administration, REDCap, versions control, and even Python, PHP, and Javascript
coding.  Any or all of these roles may overlap depending on skill set and team
size.


### Developer

The developer role is occupied by someone with software development skills, MacOSX/Linux command line skills and some script skills in BASH and Python. Minimal SQL and REDCap skills are also required to do the job well.  This person is responsible for testing and updating software packaging and deployment scripts. The scripts are written in Python or BASH and are tailored to building and deploying REDCap in a Debian Linux environment. Common tasks will include the update of a package with a new version of REDCap or a new version of a REDCap extension. Good analytical skills are required to determine if the packaging and deployment scripts are working correctly and if the deployed instance of REDCap is working correctly. This person would diagnose and correct failing scripts.  This role would also author new packaging and deployment scripts for new REDCap extensions.

This person would curate all of this work in version control to assure the complete history of changes is well documented. This person would follow a documented software development workflow with tagged releases and a change log to summarize the changes in each release.


### REDCap Staff

The role of _REDCap staff_ requires good REDCap skills and written communication skills. Minimal web site authoring skills would be helpful for the dissemination of documentation and announcements. This person will evaluate new and upgraded REDCap instances to verify normal REDCap behavior. They would do similarly for important REDCap extensions. This person will write and publish documentation about new REDCap features and announcement upgrade events to the REDCap customers.

This role would need generous permissions in the staging instance of the REDCap system used to evaluate the deploed software package.


### Systems

The role of _technical staff_ requires a person with good MacOSX/Linux command line skills and analytical skills. Experience with MySQL backup tools and REDCap would be valuable.  The person in this role will execute backups, run the deployment tools against production, and evaluate the deployment.

This role needs the permissions required to deploy to the production REDCap host and its MySQL database.

