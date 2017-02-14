# How to Deploy or Upgrade REDCap

This guide will define the fabric functions and show you how to use fabric to Package, Deploy or Upgrade REDCap.

---

## Command definitions - Public Commands  


`add_ssh_key(path, name)`  
path: the path to the file with the public key. name: the name of the user this key is tied to. This command is used to add a public key to the deploy user's list of keys. The added key should be named, in order to keep track of its user. The key must be a pub file. The list of available keys is then recreated. If any keys were removed from the deploy users ssh directory, they will no longer work for ssh.

`backup_database()`  
Create a backup mysql database from the remote host. The backup is also stored on the remote host (in the /home/<user>/ directory). The backup file will be time stamped with a name like 'redcap-dump-20170126T1620.sql' The latest backup file will be linked to name 'redcap-dump-latest.sql'.

`clean(builddir)`  
Delete the local build directory in order to avoid duplicates or any complications when creating a new redcap build. Builddir defualts to "build".

`delete_all_tables(confirm)`  
Delete existing tables, including foreign keys, from the mySQL database specified in the instance. The confirmation must be affirmative (yes, y, true) in order to execute.

`deploy(name, force)`  
Deploy a new REDCap instance defined by <name> of the package and optionally forcing cron deployment (the default is not to force cron deployment). This command runs through several steps. First, a target directory for deployent is created. The package moved to the target directory and deployed. Then some server setup variables are retrieved/set. A configuration file is then created. If the environment is a vagrant environment, a new database is created. Tables are made to fill the database. From there, the database is backed up and a symlink is created to the current deployed directory from the live location. The edocs folder is moved the deployed directory (visible on the live). The live REDCap url is set in the configuration table. The hook funtions location is set in the configuration table. REDCap cron configuration is set (if forced) and the configuration file is deleted.

`instance(name)`  
Specifies what instance to create using <name>. The <name> defaults to blank, and will prompt the user to provide a name if left blank. The specifics of the instance will be gleaned from the setings/<name>.ini set/established in this function.

`offline()`  
Updates the server sql configuration table and specifies that Offline State = 1. A status message of "The system is offline" is also provided to the sql config table.

`online()`  
Updates the server sql configuration table and specifies that Offline State = 0. A status message of "The system is online" is also provided to the sql config table.

`package()`  
Create a REDCap package from a redcapM.N.O.zip or redcapM.N.O_upgrade.zip. The resulting file will be named redcap-M.N.O.tgz. Where M = major release number, N = minor feature number, and O = patch/hotfix number.

`prod()`  
Declare a prod instance. It specifies that the settings file used will be prod.ini.

`setup_server()`  


`vagrant()`  

Declare a vagrant instance. It specifies that the settings file used will be vagrant.ini.