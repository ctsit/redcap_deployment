# REDCap Deployment Tools

This guide will define the fabric functions and show you how to use fabric to Package, Deploy or Upgrade REDCap.

---

## Command definitions - Public Commands  

`add_ssh_key(path, name)`  
path: the path to the file with the public key.  
name: the name of the user this key is tied to.

This command is used to add a public key to the deploy user's list of keys. The added key should be named, in order to keep track of its user. The key must be a pub file. The list of available keys is then recreated. If any keys were removed from the deploy users ssh directory, they will no longer work for ssh.

`apply_sql_to_db(sql_file)`  
sql_file: local SQL file.

Copy a local SQL file to the remote host a run it agains mysql. The configuration file (cnf) is written and destroyed during this command sequence.

`backup_database()`  

Create a backup mysql database from the remote host. The backup is also stored on the remote host (in the /home/user/directory). The backup file will be time stamped with a name like 'redcap-dump-20170126T1620.sql.gz' The latest backup file will be linked to name 'redcap-dump-latest.sql.gz'.

`clean(builddir)`  
builddir: a directory where the software package is stored

Delete the local build directory in order to avoid duplicates or any complications when creating a new redcap build. Builddir defaults to "build".

`delete_all_tables(confirm)`  
confirm: safeguard to ensure that user wants to delete all tables.

Delete existing tables, including foreign keys, from the mySQL database specified in the instance. The confirmation must be affirmative (yes, y, true) in order to execute.

`delete_remote_my_cnf`  

Delete .my.cnf from the deploy users home directory. This is the database configuration file.

`deploy(name, force)`  
name: name of the packaged RC software to deploy
force: if affirmative

Deploy a new REDCap instance using a redcap package defined by `name`. If `force` is set, a REDCap cron entry will be created for this instance. Use `force` with the greatest cautiously when a clone of another instance.  REDCap Cron will send out automated survey invititon if any are due.

`instance(name)`  
name: specifies what instance to create

Set up deployment for vagrant/stage/prod server. `name` defaults to blank, and will prompt the user to provide a name if left blank. The specifics of the instance will be gleaned from the setings/`name`.ini set/established in this function.

`offline()`  

Moves the REDCap instance into an offline state with a status message of "The system is offline".

`online()`  

Moves the REDCap instance into an online state.

`package(redcap_zip)`  
redcap_zip: the zipped redcap software you want to re-package into a .tgz file.

Create a REDCap package from a redcapM.N.O.zip or redcapM.N.O_upgrade.zip. The resulting file will be named redcap-M.N.O.tgz. Where M = major release number, N = minor feature number, and O = patch/hotfix number. If unspecified, `redcap_zip` defaults to the latest zipped version of redcap in the present directory.

`prod()`  

Declare a prod instance. It specifies prod.ini to be used as the settings file. This is the same as calling instance(prod).

`setup_server()`  

Create the 'deploy' user and set up the web space and backup web space. This command requires sudo privileges on the target host.

`stage()`  

Declare a stage instance. It specifies stage.ini to be used as the settings file. This is the same as calling instance(stage).

`test(warn_only)`  
warn_only: a boolean value that will abort upon failure if warn_only=False or will issue a warning if warn_only=True.  

Run all tests against a running REDCap instance.

`upgrade(name)`  
name: name of the tgz package to be used to upgrade the REDCap instance  

Upgrade an existing REDCap instance using the package specified in `name`. The named package *must* have been built from a *upgrade* package.

`vagrant()`  

Declare a development instance. It specifies vagrant.ini to be used as the settings file. This is the same as calling instance(vagrant).
