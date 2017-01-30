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
from tempfile import mkstemp
import re
import json
import fnmatch

def make_builddir(builddir="build"):
    '''
    Create the local build directory.
    '''

    with settings(warn_only=True):
        if local("test -e %s" % builddir).failed:
            local("mkdir %s" % builddir)
        else:
            print ("Directory %s already exists!" % builddir)

@task
def clean(builddir="build"):
    '''
    Clean the local build directory.
    '''
    local("rm -rf %s" % builddir)

def latest_redcap(sourcedir="."):
    env.latest_redcap = local("ls %s/redcap*.zip | grep 'redcap[0-9]\{1,2\}\.[0-9]\{1,2\}\.[0-9]\{1,2\}\.zip' | sort -n | tail -n 1" % sourcedir, capture=True).stdout
    return (env.latest_redcap)

def extract_redcap(redcap_zip="."):
    print (redcap_zip)
    #TODO determine if redcap_zip is a RC.zip or a path
    with settings(warn_only=True):
        if local("test -d %s" % redcap_zip).succeeded:
            redcap_path = latest_redcap(redcap_zip)
        elif local("test -e %s" % redcap_zip).succeeded:
            redcap_path = redcap_zip
        else:
            abort("The redcap version specified is neither a zip file nor a path.")
    print (redcap_path)
    match = re.search(r"(redcap)(\d+.\d+.\d+)(|_upgrade)(.zip)", redcap_path)
    print(match.group(2))
    env.redcap_version = match.group(2)
    local("unzip -qo %s -d %s" % (redcap_path, env.builddir))

def deploy_hooks_framework_into_build_space(target_within_build_space="redcap/hooks/"):
    """
    Deploy UF's REDCap hooks framework
    """
    # make sure the target directory exists
    source_dir = env.hook_framework_deployment_source
    this_target ='/'.join([env.builddir, target_within_build_space])
    deploy_extension_to_build_space(source_dir, this_target)


def deploy_hooks_into_build_space(target_within_build_space="redcap/hooks/library"):
    """
    Deploy each extension into build space by running its own deploy.sh.
    Lacking a deploy.sh, copy the extension files to the build space.
    For each extension run test.sh if it exists.
    """
    # make sure the target directory exists
    extension_dir_in_build_space='/'.join([env.builddir, target_within_build_space])
    with settings(warn_only=True):
        if local("test -d %s" % extension_dir_in_build_space).failed:
            local("mkdir -p %s" % extension_dir_in_build_space)

    # For each type of hook, make the target directory and deploy its children
    for hooktype in os.listdir(env.hooks_deployment_source):
        # make the target directory
        hooktype_fp_in_src = '/'.join([env.hooks_deployment_source, hooktype])
        if os.path.isdir(hooktype_fp_in_src):
            # file is a hook type
            hooktype_fp_in_target = '/'.join([extension_dir_in_build_space, hooktype])
            if not os.path.exists(hooktype_fp_in_target):
                os.mkdir(hooktype_fp_in_target)

            # locate every directory in the source that matches the pattern hooks_deployment_source/<hooktype>/*
            for hook in os.listdir(hooktype_fp_in_src):
                hook_fp_in_src = '/'.join([hooktype_fp_in_src,hook])
                if os.path.isdir(hook_fp_in_src):
                    deploy_extension_to_build_space(hook_fp_in_src, hooktype_fp_in_target)

def deploy_plugins_into_build_space(target_within_build_space="/redcap/plugins"):
    """
    Deploy each extension into build space by running its own deploy.sh.
    Lacking a deploy.sh, copy the extension files to the build space.
    For each extension run test.sh if it exists.
    """
    # make sure the target directory exists
    extension_dir_in_build_space=env.builddir + target_within_build_space
    with settings(warn_only=True):
        if local("test -d %s" % extension_dir_in_build_space).failed:
            local("mkdir -p %s" % extension_dir_in_build_space)

    # locate every directory plugins_deployment_source/*
    for (dirpath, dirnames, filenames) in os.walk(env.plugins_deployment_source):
        for dir in dirnames:
            source_dir = '/'.join([dirpath,dir])
            this_target = os.path.join(extension_dir_in_build_space, dir)
            deploy_extension_to_build_space(source_dir, this_target)

def deploy_extension_to_build_space(source_dir="", build_target=""):
    if not os.path.exists(build_target):
        os.mkdir(build_target)

    # run the deployment script
    this_deploy_script = os.path.join(source_dir,'deploy.sh')
    if os.path.isfile(this_deploy_script):
        local("bash %s %s" % (this_deploy_script, build_target))
    else:
        # copy files to target
        local("cp %s/* %s" % (source_dir, build_target))

    # run test deployment script
    this_test_script = os.path.join(source_dir,'test.sh')
    if os.path.isfile(this_test_script):
        local("bash %s " % this_test_script)


##########################
def write_my_cnf():
    _, file = mkstemp()
    f = open(file, 'w')
    f.write("[mysqldump]" +"\n")
    f.write("user=" + env.database_user +"\n")
    f.write("password=" + env.database_password +"\n")
    f.write("" +"\n")
    f.write("[client]" +"\n")
    f.write("user=" + env.database_user +"\n")
    f.write("password=" + env.database_password +"\n")
    f.write("database=" + env.database_name +"\n")
    f.close()
    return(file)

def write_remote_my_cnf():
    file = write_my_cnf()
    with settings(user=env.deploy_user):
        put(file, '/home/%s/.my.cnf' % get_config('deploy_user'), use_sudo=False)
    os.unlink(file)

def delete_remote_my_cnf():
    my_cnf = '/home/%s/.my.cnf' % get_config('deploy_user')
    with settings(user=env.deploy_user):
        if run("test -e %s" % my_cnf).succeeded:
            run('rm -rf %s' % my_cnf)

def timestamp():
    return(datetime.now().strftime("%Y%m%dT%H%M%Z"))

@task(alias='backup')
def backup_database():
    '''
    Backup a mysql database from the remote host.

    The backup file will be time stamped with a name like 'redcap-dump-20170126T1620.sql'
    The latest backup file will be linked to name 'redcap-dump-latest.sql'
    '''
    write_remote_my_cnf()
    now = timestamp()
    with settings(user=env.deploy_user):
        run("mysqldump --skip-lock-tables -u %s -h %s %s > redcap-dump-%s.sql" % \
            (env.database_user, env.database_host, env.database_name, now))
        run("ln -sf redcap-dump-%s.sql redcap-dump-latest.sql" % now)
    delete_remote_my_cnf()

##########################

@task
def package(redcap_zip="."):
    """
    Create a REDCap package from a redcapM.N.O.zip or redcapM.N.O_upgrade.zip

    The resulting file will be named redcap-M.N.O.tgz
    """

    # Build the app
    clean(env.builddir)
    make_builddir(env.builddir)
    extract_redcap(redcap_zip)
    deploy_plugins_into_build_space()
    deploy_hooks_into_build_space()
    deploy_hooks_framework_into_build_space()
    apply_patches()
    add_db_upgrade_script()

    # Get variables to tell us where to write the package
    env.package_name = '%(project_name)s-%(redcap_version)s.tgz' % env
    cwd = os.getcwd()
    # create the package
    local("cd %s && tar -cz --exclude='.DS_Store' \
    -f %s/%s \
    redcap" % (env.builddir, cwd, env.package_name))

def update_redcap_connection(db_settings_file="database.php", salt="abc"):
    """
    Update the database.php file with settings from the chosen environment
    """

    redcap_database_settings_path = "/".join([env.backup_pre_path, env.remote_project_name, db_settings_file])
    with settings(user=env.deploy_user):
        run('echo \'$hostname   = "%s";\' >> %s' % (env.database_host, redcap_database_settings_path))
        run('echo \'$db   = "%s";\' >> %s' % (env.database_name, redcap_database_settings_path))
        run('echo \'$username   = "%s";\' >> %s' % (env.database_user, redcap_database_settings_path))
        run('echo \'$password   = "%s";\' >> %s' % (env.database_password, redcap_database_settings_path))
        run('echo \'$salt   = "%s";\' >> %s' % (salt, redcap_database_settings_path))

def create_database():
    '''
    Create an empty database in MySQL dropping the existing database if need be.
    '''

    # Only run on a local testing environment
    if not env.vagrant_instance:
        abort("create_database can only be run against the Vagrant instance")

    # generate the DROP/CREATE command
    create_database_sql="""
    DROP DATABASE IF EXISTS %(database_name)s;
    CREATE DATABASE %(database_name)s;

    GRANT
        SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, EXECUTE, CREATE VIEW, SHOW VIEW
    ON
        %(database_name)s.*
    TO
        '%(database_user)s'@'%(database_host)s'
    IDENTIFIED BY
        '%(database_password)s';""" % env

    # run the DROP/CREATE command as root
    with settings(user=env.deploy_user):
        run('echo "%s" | mysql -u root -p%s' % (create_database_sql, env.database_root_password))


def is_affirmative(response):
    """
    Turn strings that mean 'yes' into a True value, else False
    """

    if  re.match("^(force|true|t|yes|y)$", response, re.IGNORECASE):
        return(True)
    else:
        return(False)


@task
def delete_all_tables(confirm=""):
    """
    Delete all tables for the database specified in the instance. You must confirm this command.
    """
    if is_affirmative(confirm):
        write_remote_my_cnf()
        with settings(user=env.deploy_user):
            run("mysqldump --add-drop-table --no-data --single-transaction --databases %s | grep -e '^DROP \| FOREIGN_KEY_CHECKS' | mysql %s" \
                % (env.database_name, env.database_name))
        delete_remote_my_cnf()
    else:
        print "\nProvide a confirmation string (e.g. 'y', 'yes') if you want to delete all MySQL tables for this instance."


def set_redcap_base_url():
    """
    Set the REDCap base url
    """

    set_redcap_config('redcap_base_url', env.url_of_deployed_app)

def set_redcap_config(field_name="", value=""):
    """
    Update a single values in the redcap config table
    """
    with settings(user=env.deploy_user):
        run('echo "update redcap_config set value=\'%s\' where field_name = \'%s\';" | mysql' % (value, field_name))

def set_hook_functions_file():
    """
    Sets the hook_functions_file
    """
    value = '%s/%s' % (env.live_project_full_path,env.hooks_framework_path)
    set_redcap_config('hook_functions_file',value)

def create_redcap_tables(resource_path = "Resources/sql"):
    """
    Create redcap tables via the remote host
    """
    print("Creating redcap tables")
    redcap_sql_root_dir = os.path.join(env.backup_pre_path,env.remote_project_name)
    with settings(user=env.deploy_user):
        redcap_name = run("ls %s | grep 'redcap_v[0-9]\{1,2\}\.[0-9]\{1,2\}\.[0-9]\{1,2\}' | sort -n | tail -n 1" % redcap_sql_root_dir)
    redcap_sql_dir = os.path.join(redcap_sql_root_dir,redcap_name,resource_path)
    match = re.search('redcap_v(\d+.\d+.\d+)', redcap_name)
    version = match.group(1)
    with settings(user=env.deploy_user):
        run('mysql -u%s -p%s %s < %s/install.sql' % (env.database_user, env.database_password, env.database_name, redcap_sql_dir))
        run('mysql -u%s -p%s %s < %s/install_data.sql' % (env.database_user,env.database_password,env.database_name, redcap_sql_dir))
        run('mysql -u%s -p%s %s -e "UPDATE %s.redcap_config SET value = \'%s\' WHERE field_name = \'redcap_version\' "' % (env.database_user,env.database_password,env.database_name, env.database_name,version))

        files=run('ls -v1 %s/create_demo_db*.sql' % redcap_sql_dir)
        for file in files.splitlines():
            print("Executing sql file %s" % file)
            run('mysql -u%s -p%s %s < %s' % (env.database_user, env.database_password,env.database_name,file))

def apply_upgrade_sql():
    """
    Copy upgrade.sql to the remote host and run upgrade.sql file

    TODO: Delete this function?
    """
    upgrade_file = "upgrade.sql"
    with settings(user=env.deploy_user):
        redcap_upgrade_sql_path = run('mktemp')
    if local('test -e %s' % upgrade_file).succeeded:
        with settings(user=env.deploy_user):
            put(upgrade_file, redcap_upgrade_sql_path)
            if run('mysql < %s' % redcap_upgrade_sql_path).succeeded:
                run('rm %s' % redcap_upgrade_sql_path)

def apply_patches():
    for repo in json.loads(env.patch_repos):
        tempdir = local('mktemp -d 2>&1', capture = True)
        local('git clone %s %s' % (repo,tempdir))
        local('%s/deploy.sh %s/redcap %s' % (tempdir, env.builddir, env.redcap_version))
        local('rm -rf %s' % tempdir)

def add_db_upgrade_script():
    target_dir = '/'.join([env.builddir, env.project_name, "redcap_v%s" % env.redcap_version])
    print target_dir
    local('cp deploy/files/generate_upgrade_sql_from_php.php %s' % target_dir)


def configure_redcap_cron(force_deployment_of_redcap_cron=False):
    crond_for_redcap = '/etc/cron.d/%s' % env.project_name
    with settings(warn_only=True):
        if run("test -e %s" % crond_for_redcap).failed or force_deployment_of_redcap_cron:
            sudo('echo "# REDCap Cron Job (runs every minute)" > %s' % crond_for_redcap)
            sudo('echo "* * * * * root /usr/bin/php %s/cron.php > /dev/null" >> %s' \
                % (env.live_project_full_path, crond_for_redcap))


def move_edocs_folder():
    """
    Move the redcap/edocs folder out of web space.
    """
    default_edoc_path = '%s/edocs' % env.live_project_full_path
    with settings(user=env.deploy_user):
        with settings(warn_only=True):
            if run("test -e %s" % env.edoc_path).succeeded:
                set_redcap_config('edoc_path',env.edoc_path)
            if run("test -e %s" % default_edoc_path).succeeded:
                with settings(warn_only=False):
                    file_name = run('ls -1 %s' % default_edoc_path)
                    if file_name == "index.html":
                        run('rm -r %s' % default_edoc_path)


def extract_version_from_string(string):
    '''
    extracts version number from string
    '''
    match = re.search(r"(\d+\.\d+\.\d+)", string)
    version=match.group(1)
    return version

######################

@task
def upgrade(name):
    '''
    Upgrade an existing redcap instance using the <name> package.

    This input file should be in the TGZ format
    as packaged by this fabfile
    '''

    make_upload_target()
    copy_running_code_to_backup_dir()
    upload_package_and_extract(name)
    write_remote_my_cnf()
    offline()
    move_software_to_live()
    new = extract_version_from_string(name)
    old = get_current_redcap_version()
    apply_incremental_db_changes(old,new)
    delete_remote_my_cnf()
    #online()

def make_upload_target():
    '''
    Make the directory from which new software will be deployed,
    e.g., /var/www.backup/redcap-20160117T1543/
    '''
    env.upload_target_backup_dir = '/'.join([env.upload_project_full_path, env.remote_project_name])
    with settings(user=env.deploy_user):
        run("mkdir -p %(upload_target_backup_dir)s" % env)

def copy_running_code_to_backup_dir():
    '''
    Copy the running code e.g. /var/www/redcap/* to the directory from which the
    the new software will be deployed, e.g., /var/www.backup/redcap-20160117T1543/.
    This will allow the new software to be overlain on the old software without
    risk of corrupting the old software.
    '''
    with settings(user=env.deploy_user):
        with settings(warn_only=True):
            if run("test -e %(live_project_full_path)s/cron.php" % env).succeeded:
                run("cp -r -P %(live_project_full_path)s/* %(upload_target_backup_dir)s" % env)

def upload_package_and_extract(name):
    '''
    Upload the redcap package and extract it into the directory from which new
    software will be deployed, e.g., /var/www.backup/redcap-20160117T1543/
    '''
    # NOTE: run as $ fab <env> package make_upload_target upe ...necessary env
    # variables are set by package and make_upload_target funcitons
    with settings(user=env.deploy_user):
        # Make a temp folder to upload the tar to
        temp1 = run('mktemp -d')
        put(name, temp1)
        # Test where temp/'receiving' is
        temp2 = run('mktemp -d')
        # Extract in temp ... -C specifies what directory to extract to
        # Extract to temp2 so the tar is not included in the contents
        run('tar -xzf %s/%s -C %s' % (temp1, name, temp2))
        # Transfer contents from temp2/redcap to ultimate destination
        with settings(warn_only=True):
            if run('test -d %s/webtools2/pdf/font/unifont' % env.upload_target_backup_dir).succeeded:
                run('chmod ug+w %s/webtools2/pdf/font/unifont/*' % env.upload_target_backup_dir)
        run('rsync -rc %s/redcap/* %s' % (temp2, env.upload_target_backup_dir))
        # Remove the temp directories
        run('rm -rf %s %s' % (temp1, temp2))

@task
def offline():
    '''
    Take REDCap offline
    '''

    change_online_status('Offline')

def move_software_to_live():
    '''Replace the symbolic link to the old code with symbolic link to new code.'''
    with settings(user=env.deploy_user):
        with settings(warn_only=True):
            if run("test -d %(live_project_full_path)s" % env).succeeded:
                # we need to back this directory up on the fly, destroy it and then symlink it back into existence
                with settings(warn_only=False):
                    new_backup_dir = env.upload_target_backup_dir + "-previous"
                    run("mkdir -p %s" % new_backup_dir)
                    run("cp -rf -P %s/* %s" % (env.live_project_full_path, new_backup_dir))
                    run("rm -rf  %s" % env.live_project_full_path)

        # now switch the new code to live
        run('ln -s %s %s' % (env.upload_target_backup_dir,env.live_project_full_path))

def convert_version_to_int(version):
    """
    Convert a redcap version number to integer
    """
    version = int("%d%02d%02d" % tuple(map(int,version.split('.'))))
    return version


def get_current_redcap_version():
    '''
    gets the current redcap version from database
    '''
    with settings(user=env.deploy_user):
        with hide('output'):
            current_version = run('mysql -s -N -e "SELECT value from redcap_config WHERE field_name=\'redcap_version\'"')
    return current_version

def apply_incremental_db_changes(old, new):
    '''
    Upgrade the database from the <old> REDCap version to the <new> version.

    Applying the needed upgrade_M.NN.OO.sql and upgrade_M.NN.OO.ph files in
    sequence. The arguments old and new must be version numbers (i.e., 6.11.5)
    '''
    old = convert_version_to_int(old)
    redcap_sql_dir = '/'.join([env.live_pre_path, env.project_path, 'redcap_v' + new, 'Resources/sql'])
    with settings(user=env.deploy_user):
        with hide('output'):
            files = run('ls -1 %s/upgrade_*.sql %s/upgrade_*.php  | sort --version-sort ' % (redcap_sql_dir, redcap_sql_dir))
    path_to_sql_generation = '/'.join([env.live_pre_path, env.project_path, 'redcap_v' + new, 'generate_upgrade_sql_from_php.php'])
    for file in files.splitlines():
        match = re.search(r"(upgrade_)(\d+.\d+.\d+)(.)(php|sql)", file)
        version = match.group(2)
        version = convert_version_to_int(version)
        if(version > old):
            if fnmatch.fnmatch(file, "*.php"):
                print (file + " is a php file!\n")
                with settings(user=env.deploy_user):
                    run('php %s %s | mysql' % (path_to_sql_generation,file))
            else:
                print("Executing sql file %s" % file)
                with settings(user=env.deploy_user):
                    run('mysql < %s' % file)
    # Finalize upgrade
    set_redcap_config('redcap_last_install_date', datetime.now().strftime("%Y-%m-%d"))
    set_redcap_config('redcap_version', new)

@task
def online():
    '''
    Put REDCap back online
    '''

    change_online_status('Online')

def change_online_status(state):
    '''
    Set the online/offline status with <state>.
    '''

    with settings(user=env.deploy_user):
        if state == "Online":
            offline_binary = 0
            offline_message = 'The system is online.'
        elif state == "Offline":
            offline_binary = 1
            offline_message = 'The system is offline.'
        else:
            abort("Invald state provided. Specify 'Online' or 'Offline'.")
        if run('test -e ~/.my.cnf').failed:
            write_remote_my_cnf()
            set_redcap_config('system_offline', '%s' % offline_binary)
            set_redcap_config('system_offline_message', '%s' % offline_message)
            delete_remote_my_cnf()
        else:
            set_redcap_config('system_offline', '%s' % offline_binary)
            set_redcap_config('system_offline_message', '%s' % offline_message)

##########################

def get_config(key, section="instance"):
    return config.get(section, key)

def define_default_env(settings_file_path="settings/defaults.ini"):
    """
    This function sets up some global variables
    """

    #first, copy the secrets file into the deploy directory
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

    #first, copy the secrets file into the deploy directory
    if os.path.exists(settings_file_path):
        config.read(settings_file_path)
    else:
        print("The secrets file path cannot be found. It is set to: %s" % settings_file_path)
        abort("Secrets File not set")

    if get_config('deploy_user') != "":
        env.user = get_config('deploy_user')

    section="instance"
    for (name,value) in config.items(section):
        env[name] = value
    # Set variables that do not have corresponding values in vagrant.ini file
    env.live_project_full_path = get_config('live_pre_path') + "/" + get_config('project_path') #
    env.backup_project_full_path = get_config('backup_pre_path') + "/" + get_config('project_path')
    env.upload_project_full_path = get_config('backup_pre_path')

    env.hosts = [get_config('host')]
    env.port = get_config('host_ssh_port')

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
def instance(name = ""):
    """
    Set up deployment for vagrant/stage/prod server
    """

    if(name == ""):
        abort("Please provide an instance name")
    settings_file_path = 'settings/%s.ini' % name
    if(name == 'vagrant'):
        env.vagrant_instance = True
    define_env(settings_file_path)

@task
def deploy(name,force=""):
    """
    Deploy a new REDCap instance defined by <package_name>, optionally forcing redcap cron deployment

    """
    make_upload_target()
    upload_package_and_extract(name)
    update_redcap_connection()
    write_remote_my_cnf()
    if env.vagrant_instance:
        create_database()
    create_redcap_tables()
    move_software_to_live()
    move_edocs_folder()
    set_redcap_base_url()
    set_hook_functions_file()
    force_deployment_of_redcap_cron = is_affirmative(force)
    configure_redcap_cron(force_deployment_of_redcap_cron)
    delete_remote_my_cnf()
    #TODO: Run tests


#############################################################################
"""
The following functions are admin level functions which will alter the server.
They will need to be run with the admin=True flag when setting up the env
"""

def setup_webspace():
    """
    Make live web space (e.g., www) and backup web space (e.g. www.backup) as root user
    """
    #Change the permissions to match the correct user and group
    sudo("mkdir -p %(backup_project_full_path)s" % env)

    sudo("chown -R %s.%s %s" % (env.deploy_user, env.deploy_group, env.backup_pre_path))
    sudo("chmod -R 775 %s"  % (env.backup_pre_path))

    sudo("chown -R %s.%s %s" % (env.deploy_user, env.deploy_group, env.live_pre_path))
    sudo("chmod -R 775 %s"  % (env.live_pre_path))

    sudo("mkdir -p %s" % env.edoc_path)

@task
def setup_server():
    """
    Create the 'deploy' user and set up the web space and backup web space
    """
    create_deploy_user_with_ssh()
    setup_webspace()

def create_deploy_user_with_ssh():
    """
    Create 'deploy' user as root.

    This function will create the deployment user. It will place
    this user in the group assigned.
    """

    random_password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32))
    #sudo('getent passwd %s > /dev/null; if [ $? -ne 0 ]; then; useradd -m -b /home -u 800 -g %s -s /bin/bash -c "deployment user" %s -p %s; else; usermod -g %s %s ;fi' % (env.user, env.group, env.user, random_password))

    # Make a deploy user with the right group membership
    with settings(warn_only=True):
        if (sudo('getent passwd %s > /dev/null' % env.deploy_user).return_code == 0):
            sudo('usermod -g %s %s' % (env.deploy_group, env.deploy_user))
        else:
            sudo('useradd -m -b /home -u 800 -g %s -s /bin/bash -c "deployment user" %s -p %s' \
                % (env.deploy_group, env.deploy_user, random_password))

    with settings(user=env.deploy_user):
        with settings(warn_only=True):
            if (run('test -d ~/.ssh/keys').failed):
                run('mkdir -p ~/.ssh/keys')
                if run("test -e ~/.ssh/authorized_keys").succeeded:
                    run('cp ~/.ssh/authorized_keys ~/.ssh/keys/default.pub')
                else:
                    put(env.pubkey_filename,"~/.ssh/keys/%s.pub" % env.user)

    update_ssh_permissions()

    #TODO: automatically add ssh key or prompt

def update_ssh_permissions():
    """
    Adjust perms on the 'deploy' user's ssh keys
    """

    #create SSH directory
    with settings(user=env.deploy_user):
        run('chmod 700 /home/%s/.ssh' % env.deploy_user)
        run('chmod 644 /home/%s/.ssh/authorized_keys' % env.deploy_user)
        run('chmod -R 700 /home/%s/.ssh/keys' % env.deploy_user)
        #run('chown -R %s.%s /home/%s' % (env.deploy_user, env.deploy_group, env.deploy_user))

def add_new_ssh_key_as_string(ssh_public_key_string, name):
    """
    Add an ssh key to the deploy user's authorized keys from a string.

    TODO: validate string is valid ssh key

    ssh_public_key_string: the actual public key string
    name: the name of the user this key is tied to
    """

    ssh_key = ssh_public_key_string
    copy_ssh_key_to_host(ssh_key,name)
    rebuild_authorized_keys()
    update_ssh_permissions()

@task
def add_ssh_key(path, name):
    """
    Add an ssh key to the deploy user's authorized keys by providing <path>,<name>

    path: the path to the file with the public key.
    name: the name of the user this key is tied to.
    """
    ssh_key = open(path, 'r').read()
    copy_ssh_key_to_host(ssh_key, name)
    rebuild_authorized_keys()
    update_ssh_permissions()

def copy_ssh_key_to_host(ssh_key, name):
    """
    Creates a new pub file with the name provided and
    ssh key inside. Ships that pub file to the deploy
    users ssh directory

    ssh_key: String of ssh_key to create a new pub file from
    name: the name of the user this key is tied to
    """
    with settings(user=env.deploy_user):
        pub_file = open('%s.pub' % name, 'w')
        pub_file.write(ssh_key)
        pub_file.close()
        put('%s.pub' % name, '/home/%s/.ssh/keys/' % env.user)

def rebuild_authorized_keys():
    """
    Take all the current pub files and recreate authorized_keys from them.
    If any of the pub files are removed, they get removed from the authorized keys
    and can no longer ssh in.
    """
    with settings(user=env.deploy_user):
        run('cat `find /home/%s/.ssh/keys/ -type f` > tmpfile' % env.deploy_user)
        run('cp tmpfile /home/%s/.ssh/authorized_keys' % env.deploy_user)
        run('rm tmpfile')

config = configparser.ConfigParser()
default_settings_file_path = 'settings/defaults.ini' #path to where app is looking for settings.ini
define_default_env(default_settings_file_path) # load default settings
time = timestamp()
env.remote_project_name = '%s-%s' % (env.project_name,time)
