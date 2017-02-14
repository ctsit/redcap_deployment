# How to Deploy or Upgrade REDCap

This guide will define the fabric functions and show you how to use fabric to Package, Deploy or Upgrade REDCap.

---

## Command definitions - Public Commands  

`add_ssh_key(path, name)`  
path: the path to the file with the public key.  
name: the name of the user this key is tied to.
* This command is used to add a public key to the deploy user's list of keys. The added key should be named, in order to keep track of its user. The key must be a pub file. The list of available keys is then recreated. If any keys were removed from the deploy users ssh directory, they will no longer work for ssh.

`apply_sql_to_db(sql_file)`  
sql_file: local SQL file.
* Copy a local SQL file to the remote host a run it agains mysql. The configuration file (cnf) is written and destroyed during this command sequence.

`backup_database()`  
* Create a backup mysql database from the remote host. The backup is also stored on the remote host (in the /home/user/directory). The backup file will be time stamped with a name like 'redcap-dump-20170126T1620.sql' The latest backup file will be linked to name 'redcap-dump-latest.sql'.

`clean(builddir)`  
builddir: a directory where the software package is stored
* Delete the local build directory in order to avoid duplicates or any complications when creating a new redcap build. Builddir defualts to "build".

`delete_all_tables(confirm)`  
confirm: safeguard to ensure that user wants to delete all tables.
* Delete existing tables, including foreign keys, from the mySQL database specified in the instance. The confirmation must be affirmative (yes, y, true) in order to execute.

`delete_remote_my_cnf`  
* Delete .my.cnf from the deploy users home directory. This is the database configuration file.

`deploy(name, force)`  
name: name of the packaged RC software to deploy
force: if affirmative
* Deploy a new REDCap instance defined by [name] of the package and optionally forcing cron configuration (the default is not to force cron configuration). This command runs through several steps. First, a target directory for deployent is created. The package moved to the target directory and deployed. Then some server setup variables are retrieved/set. A configuration file is then created. If the environment is a vagrant environment, a new database is created. Tables are made to fill the database. From there, the database is backed up and a symlink is created to the current deployed directory from the live location. The edocs folder is moved the deployed directory (visible on the live). The live REDCap url is set in the configuration table. The hook funtions location is set in the configuration table. REDCap cron configuration is set (if forced) and the configuration file is deleted.

`instance(name)`  
name: specifies what instance to create
* Set up deployment for vagrant/stage/prod server. The [name] defaults to blank, and will prompt the user to provide a name if left blank. The specifics of the instance will be gleaned from the setings/[name].ini set/established in this function.

`offline()`  
* Updates the server sql configuration table and specifies that Offline State = 1. A status message of "The system is offline" is also provided to the sql config table.

`online()`  
* Updates the server sql configuration table and specifies that Offline State = 0. A status message of "The system is online" is also provided to the sql config table.

`package(redcap_zip)`  
redcap_zip: the zipped redcap software you want to package
* Create a REDCap package from a redcapM.N.O.zip or redcapM.N.O_upgrade.zip. The resulting file will be named redcap-M.N.O.tgz. Where M = major release number, N = minor feature number, and O = patch/hotfix number. If unspecified, [redcap_zip] defaults to the latest zipped version of redcap in the present directory.

`prod()`  
* Declare a prod instance. It specifies prod.ini to be used as the settings file. This is the same as calling instance(prod).

`setup_server()`  
* Create the 'deploy' user and set up the web space and backup web space. This includes creating a live web space and backing up the previous web space. The deploy user is also created with root ssh permisions.

`stage()`  
* Declare a stage instance. It specifies stage.ini to be used as the settings file. This is the same as calling instance(stage).

`test(warn_only)`  
warn_only: a boolean value that will abort upon failure if warn_only=False or will issue a warning if warn_only=True.  
* Run all tests against a running REDCap instance.

`upgrade(name)`  
name: name of the tgz package of the REDCap software of the version of choice.  
* Upgrade an existing redcap instance using the [name] package. This includes making the upload target directory, the backkup directory, the deployment directory, writing the cnf file, taking the current system offline, creating a symlink to the deployment directory, applying increme tal changes from the previous version to the deployment version, bringing the system back online, running tests, and deleting the configuratio file. 

`vagrant()`  
* Declare a development instance. It specifies vagrant.ini to be used as the settings file. This is the same as calling instance(vagrant).

Declare a vagrant instance. It specifies that the settings file used will be vagrant.ini.