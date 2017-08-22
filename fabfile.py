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
from fabric.utils import abort
try:
    import configparser
except:
    from six.moves import configparser
import string, random, os
import server_setup
import package
import deploy
import upgrade
import utility
import utility_redcap
import hook
import plugins
import module

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
    utility.apply_local_sql_to_db(sql_file)


@task
def offline():
    """
    Take REDCap offline
    """

    upgrade.offline()


@task
def online():
    """
    Put REDCap back online
    """

    upgrade.online()


@task
def activate_hook(hook_function="", hook_name="", pid=""):
    """
    Activate the hook `hook_name` as type of `hook_function` for the project named by `pid`.

    If PID is omitted, the hook will be activated globally.

    :param hook_function: one of the 13 named REDCap 'hook functions'
    :param hook_name: the name of the hook file with or without the .php extension
    :param pid: the ID of the project on which this hook should be activated. If left blank the hook will be activated globally
    :return:
    """
    redcap_root = env.live_project_full_path
    hook.activate(hook_function, hook_name, redcap_root, pid)


@task
def test_hook(hook_function="", hook_path=""):
    """
    Symbolically link a host file that contains a redcap hook into the hooks library space and activate that hook globally

    :param hook_function: one of the 13 named REDCap 'hook functions'
    :param hook_path: path to hook file relative to VagrantFile
    :return:
    """
    hook.test(hook_function, hook_path)


@task
def test_plugin(plugin_path=""):
    """
    Symbolically link a host file that contains a redcap plugin into the ./redcap/plugins folder

    :param plugin_path: path to plugin folder relative to VagrantFile
    :return:
    """
    plugins.test(plugin_path)


@task
def test(warn_only=False):
    """
    Run all tests against a running REDCap instance
    """
    return(utility_redcap.test(warn_only))

@task
def test_module(module_name):
    """
    Adds a local module located under "modules/" directory to the list of available modules on REDCap.
    """
    with settings(user=env.deploy_user):
        dest = '/'.join([env.live_project_full_path, "modules/%s" % module_name])
        if not os.path.exists(dest):
            src = "/vagrant/modules/%s" % module_name
            run("ln -s %s %s" % (src, dest))


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

    utility.get_config('deploy_user', settings_file_path)

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

    # Turn deploy_redcap_cron into a boolean
    env.deploy_redcap_cron = utility.is_affirmative(env.deploy_redcap_cron)


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
