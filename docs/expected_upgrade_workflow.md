# Expected Upgrade Workflow

The packaging and deployment tools in this repository lend themselves to a REDCap upgrade workflow.  That work flow might look something like this:

|Days Budgeted |Role  |Tasks      |
------|---------------|-----------|
|1-2  |Developer      |Develop upgrade package with REDCap code, with extensions, upgrade.sql and deployment script. Test upgrade package. Deploy to staging instance.  |
|2-3  | REDCap Staff  |Test in staging instance using manual validation procedure.  |
|1    | REDCap Staff  |Write upgrade announcement. Set upgrade date. Announce upgrade with at least 7 days notice.  |
|1-2  | REDCap Staff  |Write documents for describing new features.  |
|1-2  | REDCap Staff  |If needed, update manual validation procedure.  |
|1    |Systems / REDCap Staff  |Deploy to Prod instance. Test Prod instance. If tests fail, rollback prod.  |

## Roles

* Developer - Technical staff with MacOSX/Linux command line skills and some script skills in BASH and Python. Minimal SQL and REDCap skills are also required. Will replace redcapX.Y.Z.zip files, update extension, update and write new extension deployment scripts.
* REDCap Staff - Skilled REDCap user with comunication skills. Will evaluate normal REDCap behavior and that of important extensions. Will write documentation and announcements for REDCap customers.
* Systems - Technical staff with macosx/linux command line skills and permissions to deploy to production REDCap host and its MySql database. Will execute backups, run deployment tools, and evaluate deployment.

These roles may overlap depending on skill set and team size.
