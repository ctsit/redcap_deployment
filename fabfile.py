"""
This fab file packages, deploys, and upgrades REDCap. The fab file uses a
settings file to define the parameters of each deployed instance/environment.

Usage:

  fab package<:redcapM.N.O.zip>
  fab <instance_name> deploy<:redcap-M.N.O.tgz>
  fab <instance_name> upgrade<:redcap-M.N.O.tgz>
  fab instance:<instance_name> upgrade<:redcap-M.N.O.tgz>

Instances

Each environment is a separate REDCap instance. Each instance can be deployed
or upgraded. The valid instances are:

  vagrant - a local development instance
  stage - a staging test instance
  prod - the production instance

Each instance requires a same-named file at the local path settings/<name>.ini

The *instance* function can be used to use an arbitrary instance by providing
the instance name as a parameter to the instance function:

  fab instance:vagrant deploy:redcap-6.18.1.tgz
  fab instance:stage2 deploy:redcap-7.1.0.tgz


Deploying

When (re)deploying the instance named 'vagrant', be aware that deploy will
drop the instance database.


Upgrading

Upgrade packages must be created using one of Vanderbilt's 'upgrade' zip files
or database credentials will not be preserved.

"""

from fabric.api import *
from fabric.contrib.files import exists
from fabric.utils import abort
from datetime import datetime
import configparser, string, random, os
import re
import fnmatch
import server_setup
import package
import deploy
import utility
import utility_redcap


@task(alias='backup')
def backup_database(options=""):
    """
    Backup a mysql database from the remote host with mysqldump options in *options*.

    The backup file will be time stamped with a name like 'redcap-<instance_name>-20170126T1620.sql.gz'
    The latest backup file will be linked to name 'redcap-<instance_name>-latest.sql.gz'
    """
    utility.write_remote_my_cnf()
    now = utility.timestamp()
    with settings(user=env.deploy_user):
        run("mysqldump --skip-lock-tables %s -u %s -h %s %s | gzip > redcap-%s-%s.sql.gz" % \
            (options, env.database_user, env.database_host, env.database_name, env.instance_name, now))
        run("ln -sf redcap-%s-%s.sql.gz redcap-%s-latest.sql.gz" % (env.instance_name, now, env.instance_name))
    utility.delete_remote_my_cnf()



######################


@task
def delete_all_tables(confirm=""):
    """
    Delete all tables for the database specified in the instance. You must confirm this command.
    """
    utility.delete_all_tables(confirm)


@task
def apply_sql_to_db(sql_file=""):
    """
    Copy a local SQL file to the remote host and run it against mysql

    """
    utility.apply_sql_to_db(sql_file)


@task
def upgrade(name):
    """
    Upgrade an existing redcap instance using the <name> package.

    This input file should be in the TGZ format
    as packaged by this fabfile
    """

    utility_redcap.make_upload_target()
    copy_running_code_to_backup_dir()
    utility_redcap.upload_package_and_extract(name)
    utility.write_remote_my_cnf()
    offline()
    utility_redcap.move_software_to_live()
    new = utility.extract_version_from_string(name)
    old = utility_redcap.get_current_redcap_version()
    apply_incremental_db_changes(old,new)
    online()
    utility.delete_remote_my_cnf()


def copy_running_code_to_backup_dir():
    """
    Copy the running code e.g. /var/www/redcap/* to the directory from which the
    the new software will be deployed, e.g., /var/www.backup/redcap-20160117T1543/.
    This will allow the new software to be overlain on the old software without
    risk of corrupting the old software.
    """
    with settings(user=env.deploy_user):
        with settings(warn_only=True):
            if run("test -e %(live_project_full_path)s/cron.php" % env).succeeded:
                run("cp -r -P %(live_project_full_path)s/* %(upload_target_backup_dir)s" % env)


@task
def offline():
    """
    Take REDCap offline
    """

    change_online_status('Offline')


def apply_incremental_db_changes(old, new):
    """
    Upgrade the database from the <old> REDCap version to the <new> version.

    Applying the needed upgrade_M.NN.OO.sql and upgrade_M.NN.OO.ph files in
    sequence. The arguments old and new must be version numbers (i.e., 6.11.5)
    """
    old = utility.convert_version_to_int(old)
    redcap_sql_dir = '/'.join([env.live_pre_path, env.project_path, 'redcap_v' + new, 'Resources/sql'])
    with settings(user=env.deploy_user):
        with hide('output'):
            files = run('ls -1 %s/upgrade_*.sql %s/upgrade_*.php  | sort --version-sort ' % (redcap_sql_dir, redcap_sql_dir))
    path_to_sql_generation = '/'.join([env.live_pre_path, env.project_path, 'redcap_v' + new, 'generate_upgrade_sql_from_php.php'])
    for file in files.splitlines():
        match = re.search(r"(upgrade_)(\d+.\d+.\d+)(.)(php|sql)", file)
        version = match.group(2)
        version = utility.convert_version_to_int(version)
        if version > old:
            if fnmatch.fnmatch(file, "*.php"):
                print (file + " is a php file!\n")
                with settings(user=env.deploy_user):
                    run('php %s %s | mysql' % (path_to_sql_generation,file))
            else:
                print("Executing sql file %s" % file)
                with settings(user=env.deploy_user):
                    run('mysql < %s' % file)
    # Finalize upgrade
    utility_redcap.set_redcap_config('redcap_last_install_date', datetime.now().strftime("%Y-%m-%d"))
    utility_redcap.set_redcap_config('redcap_version', new)


@task
def online():
    """
    Put REDCap back online
    """

    change_online_status('Online')


def change_online_status(state):
    """
    Set the online/offline status with <state>.
    """

    with settings(user=env.deploy_user):
        if state == "Online":
            offline_binary = 0
            offline_message = 'The system is online.'
        elif state == "Offline":
            offline_binary = 1
            offline_message = 'The system is offline.'
        else:
            abort("Invald state provided. Specify 'Online' or 'Offline'.")

        utility.write_remote_my_cnf()
        utility_redcap.set_redcap_config('system_offline', '%s' % offline_binary)
        utility_redcap.set_redcap_config('system_offline_message', '%s' % offline_message)
        utility.delete_remote_my_cnf()


@task
def test():
    """
    Run all tests against a running REDCap instance
    """
    utility.write_remote_my_cnf()
    version = utility_redcap.get_current_redcap_version()
    utility.delete_remote_my_cnf()
    local("python tests/test.py %s/ redcap_v%s/" % (env.url_of_deployed_app,version))


##########################


def define_default_env(settings_file_path="settings/defaults.ini"):
    """
    This function sets up some global variables
    """

    # first, copy the secrets file into the deploy directory
    if os.path.exists(settings_file_path):
        config.read(settings_file_path)
    else:
        print("The secrets file path cannot be found. It is set to: %s" % settings_file_path)
        abort("Secrets File not set")

    section="DEFAULT"
    for (name,value) in config.items(section):
        env[name] = value


def define_env(settings_file_path=""):
    """
    This function sets up some global variables
    """

    # Set defaults
    env.deploy_redcap_cron = False

    # first, copy the secrets file into the deploy directory
    if os.path.exists(settings_file_path):
        config.read(settings_file_path)
    else:
        print("The secrets file path cannot be found. It is set to: %s" % settings_file_path)
        abort("Secrets File not set")

    if utility.get_config('deploy_user', settings_file_path) != "":
        env.user = utility.get_config('deploy_user',settings_file_path)

    section="instance"
    for (name,value) in config.items(section):
        env[name] = value
    # Set variables that do not have corresponding values in vagrant.ini file
    time = utility.timestamp()
    env.remote_project_name = '%s-%s' % (env.project_path,time)
    env.live_project_full_path = env.live_pre_path + "/" + env.project_path
    env.backup_project_full_path = env.backup_pre_path + "/" + env.project_path
    env.upload_project_full_path = env.backup_pre_path

    env.hosts = [env.host]
    env.port = env.host_ssh_port


@task(alias='dev')
def vagrant():
    """
    Set up deployment for vagrant
    """
    instance('vagrant')


@task
def stage():
    """
    Set up deployment for staging server
    """
    instance('stage')


@task
def prod():
    """
    Set up deployment for production server
    """
    instance('prod')


@task
def instance(name=""):
    """
    Set up deployment for vagrant/stage/prod server
    """
    if name == "":
        abort("Please provide an instance name")
    settings_file_path = 'settings/%s.ini' % name
    if name == 'vagrant':
        env.vagrant_instance = True
    else:
        env.vagrant_instance = False
    define_env(settings_file_path)


config = configparser.ConfigParser()
# path to where app is looking for settings.ini
default_settings_file_path = 'settings/defaults.ini'
# load default settings
define_default_env(default_settings_file_path)

