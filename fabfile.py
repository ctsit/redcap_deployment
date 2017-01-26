"""
This fab file packages, deploys, and upgrades REDCap. The fab file uses a
settings file to define the parameters of each deployed instance.
"""
"""
This fab file takes the QIPR project and deploys it using a provided settings file.
The settings files contains secrets, so it should be kept locally somewhere outside
the git directory. The secrets file path in this script needs to be changed to match your installation.


The basic deployment command (for staging) is "fab s deploy:0.7.0"
fab - calling the fab command
s - using the alias for stage, but could also be invoked using the whole word "stage"
deploy - function to run called deploy
:0.7.0 - run deploy and pass in the argument 0.7.0

The settings file needs to include the following fields with the correct settings:
[fabric_deploy]
deploy_user = deploy #user account associated with deploying
deploy_user_group = www-data #group that the deploy account is part of
staging_host = my.staging.host.com #staging server
production_host = my.production.host.com #production server
admin_user = superman #account with root privilege on the server
live_pre_path = /var/www #directory path leading up to the actual project directory
backup_pre_path = /var/www.backup #directory path leading up to the backup project directory
project_path = qipr/approver #where the project files are going to sit
ssh_keyfile_path = /my/user/.ssh/id_rsa #path to a local ssh private key for easy login

In order to keep deployments easy, the setups across all environments will remain
constant, with the only difference being the server ip. The directory paths will
remain constant.

There are 3 environments this script will be able to deploy to:
vagrant: includes the default admin user name and ssh key location, ip, and port
staging: this is the test live server.
production: this is the functional live server.
Each environment includes a boolean flag to enable running as root for certain
functions in this script.

Running deploy is the main function to get a version sent off to the server.

If the server is not setup for deployment yet, there are some additional helper
functions to create a deployment user and set up its permissions.
setup_server - creates the user and creates directories
setup_webspace - just creates the directories for the deploy user

There are also functions to add ssh keys to the deploy user for simple
ssh commands using a passed in string or pub file location.
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

@task
def make_builddir(builddir="build"):
    with settings(warn_only=True):
        if local("test -e %s" % builddir).failed:
            local("mkdir %s" % builddir)
        else:
            print ("Directory %s already exists!" % builddir)

@task
def clean(builddir="build"):
    local("rm -rf %s" % builddir)

@task
def latest_redcap(sourcedir="."):
    env.latest_redcap = local("ls %s/redcap*.zip | grep 'redcap[0-9]\{1,2\}\.[0-9]\{1,2\}\.[0-9]\{1,2\}\.zip' | sort -n | tail -n 1" % sourcedir, capture=True).stdout
    return (env.latest_redcap)

@task
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

@task(alias="dhfibs")
def deploy_hooks_framework_into_build_space(target_within_build_space="redcap/hooks/"):
    """
    Deploy UF's REDCap hooks framework
    """
    # make sure the target directory exists
    source_dir = env.hook_framework_deployment_source
    this_target ='/'.join([env.builddir, target_within_build_space])
    deploy_extension_to_build_space(source_dir, this_target)


@task(alias="dhibs")
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

@task(alias="dpibs")
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
    put(file, '/home/%s/.my.cnf' % get_config('deploy_user'), use_sudo=False)
    os.unlink(file)

def timestamp():
    return(datetime.now().strftime("%Y%m%dT%H%M%Z"))

@task(alias='backup')
def backup_database():
    # backup a mysql database from the remote host
    # timestamp the file and make a static symlink to the timestamped file
    write_remote_my_cnf()
    now = timestamp()
    run("mysqldump --skip-lock-tables -u %s -h %s %s > redcap-dump-%s.sql" % \
        (env.database_user, env.database_host, env.database_name, now))
    run("ln -sf redcap-dump-%s.sql redcap-dump-latest.sql" % now)

##########################

@task
def package(redcap_zip="."):
    """
    This function will go into the project directory and zip all
    of the required files
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

@task(alias='urc')
def update_redcap_connection(db_settings_file="database.php", salt="abc"):
    """This function will update the database.php file with settings
    that correspond to the chosen environment"""
    redcap_database_settings_path = "/".join([env.backup_pre_path, env.remote_project_name, db_settings_file])
    run('echo \'$hostname   = "%s";\' >> %s' % (env.database_host, redcap_database_settings_path))
    run('echo \'$db   = "%s";\' >> %s' % (env.database_name, redcap_database_settings_path))
    run('echo \'$username   = "%s";\' >> %s' % (env.database_user, redcap_database_settings_path))
    run('echo \'$password   = "%s";\' >> %s' % (env.database_password, redcap_database_settings_path))
    run('echo \'$salt   = "%s";\' >> %s' % (salt, redcap_database_settings_path))

@task
def create_database():
    """Create an empty database in MySQL dropping the existing database if need be"""

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
    run('echo "%s" | mysql -u root -p%s' % (create_database_sql, env.database_root_password))


@task
def set_redcap_base_url():
    """This function will set the redacp base url"""
    set_redcap_config('redcap_base_url', env.url_of_deployed_app)

def set_redcap_config(field_name="", value=""):
    """This function will update values for the redcap system"""
    run('echo "update redcap_config set value=\'%s\' where field_name = \'%s\';" | mysql' % (value, field_name))

@task
def set_hook_functions_file():
    """
    This function sets the hook_functions_file
    """
    value = '%s/%s' % (env.live_project_full_path,env.hooks_framework_path)
    set_redcap_config('hook_functions_file',value)

@task()
def create_redcap_tables(resource_path = "Resources/sql"):
    """
    This function creates redcap tables in remote host
    """
    print("Creating redcap tables")
    redcap_sql_root_dir = os.path.join(env.backup_pre_path,env.remote_project_name)
    redcap_name = run("ls %s | grep 'redcap_v[0-9]\{1,2\}\.[0-9]\{1,2\}\.[0-9]\{1,2\}' | sort -n | tail -n 1" % redcap_sql_root_dir)
    redcap_sql_dir = os.path.join(redcap_sql_root_dir,redcap_name,resource_path)
    match = re.search('redcap_v(\d+.\d+.\d+)', redcap_name)
    version = match.group(1)

    run('mysql -u%s -p%s %s < %s/install.sql' % (env.database_user, env.database_password, env.database_name, redcap_sql_dir))
    run('mysql -u%s -p%s %s < %s/install_data.sql' % (env.database_user,env.database_password,env.database_name, redcap_sql_dir))
    run('mysql -u%s -p%s %s -e "UPDATE %s.redcap_config SET value = \'%s\' WHERE field_name = \'redcap_version\' "' % (env.database_user,env.database_password,env.database_name, env.database_name,version))

    files=run('ls -v1 %s/create_demo_db*.sql' % redcap_sql_dir)
    for file in files.splitlines():
        print("Executing sql file %s" % file)
        run('mysql -u%s -p%s %s < %s' % (env.database_user, env.database_password,env.database_name,file))

@task
def apply_upgrade_sql():
    """
    This function copies upgrade.sql to remote vm and runs upgrade.sql file
    """
    upgrade_file = "upgrade.sql"
    redcap_upgrade_sql_path = run('mktemp')
    if local('test -e %s' % upgrade_file).succeeded:
        put(upgrade_file, redcap_upgrade_sql_path)
        if run('mysql < %s' % redcap_upgrade_sql_path).succeeded:
            run('rm %s' % redcap_upgrade_sql_path)

@task
def apply_patches():
    for repo in json.loads(env.patch_repos):
        tempdir = local('mktemp -d 2>&1', capture = True)
        local('git clone %s %s' % (repo,tempdir))
        local('%s/deploy.sh %s/redcap %s' % (tempdir, env.builddir, env.redcap_version))
        local('rm -rf %s' % tempdir)

@task
def add_db_upgrade_script():
    target_dir = '/'.join([env.builddir, env.project_name, "redcap_v%s" % env.redcap_version])
    print target_dir
    local('cp deploy/files/generate_upgrade_sql_from_php.php %s' % target_dir)

@task
def configure_redcap_cron():
    crond_for_redcap = '/etc/cron.d/redcap'
    sudo('echo "# REDCap Cron Job (runs every minute)" > %s' % crond_for_redcap)
    sudo('echo "* * * * * root /usr/bin/php %s/cron.php > /dev/null" >> %s' % (env.live_project_full_path, crond_for_redcap))

@task
def move_edocs_folder():
    """
    This function moves edocs folder out of web space
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

######################

@task
def upgrade(name):
    '''A function to upgrade an existing redcap instance using the redcap
    package named in 'name'.  This input file should be in the TGZ format
    as packaged by this fabfile'''

    # TODO: upload_package needs to be split into make_upload_target and upload_package_and_extract
    # so copy_running_code_to_backup_dir can be spliced in before extract)'''
    make_upload_target()
    copy_running_code_to_backup_dir()
    upload_package_and_extract(name)
    offline()
    move_software_to_live()
    #apply_incremental_db_changes(old,new)
    #online()

@task
def make_upload_target():
    '''
    Make the directory from which new software will be deployed,
    e.g., /var/www.backup/redcap-20160117T1543/
    '''
    env.upload_target_backup_dir = '/'.join([env.upload_project_full_path, env.remote_project_name])
    with settings(user=env.deploy_user):
        run("mkdir -p %(upload_target_backup_dir)s" % env)

@task
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

@task (alias='upe')
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
    '''use set_redcap_config to go offline'''
    set_redcap_config('system_offline', '1')
    set_redcap_config('system_offline_message', 'System Offline')

@task
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

@task
def upgrade_db():
    '''TODO: Write this later.  We will do this manually at first'''
    return 0

def convert_version_to_int(version):
    """
    Convert a redcap version number to integer
    """
    version = int("%d%02d%02d" % tuple(map(int,version.split('.'))))
    return version

@task
def apply_incremental_db_changes(old, new):
    '''update the database from current version to latest availalbe upgrade.sql
    by applying the needed upgarde_version.sql files in sequence. The arguments
    old and new will be version numbers (i.e., 6.11.5)'''

    old = convert_version_to_int(old)
    redcap_sql_dir = '/'.join([env.live_pre_path, env.project_path, 'redcap_v' + new, 'Resources/sql'])
    files = run('ls -1 %s/upgrade_*.sql %s/upgrade_*.php  | sort --version-sort ' % (redcap_sql_dir, redcap_sql_dir))
    path_to_sql_generation = '/'.join([env.live_pre_path, env.project_path, 'redcap_v' + new, 'generate_upgrade_sql_from_php.php'])
    for file in files.splitlines():
        match = re.search(r"(upgrade_)(\d+.\d+.\d+)(.)(php|sql)", file)
        version = match.group(2)
        version = convert_version_to_int(version)
        if(version > old):
            if fnmatch.fnmatch(file, "*.php"):
                print (file + " is a php file!\n")
                run('php %s %s | mysql' % (path_to_sql_generation,file))
            else:
                print("Executing sql file %s" % file)
                run('mysql < %s' % file)
    # Finalize upgrade
    set_redcap_config('redcap_last_install_date', datetime.now().strftime("%Y-%m-%d"))
    set_redcap_config('redcap_version', new)

@task
def fix_shibboleth_exceptions ():
    '''TODON'T: Don't write this. (we really need to obsolete this with ideas from redcap forum)'''
    return 0

@task
def online():
    '''use set_redcap_config to go online'''
    set_redcap_config('system_offline', '0')
    set_redcap_config('system_offline_message', 'System Online')

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

@task(alias='dev')
def vagrant(admin=False):
    """
    Set up deployment for vagrant

    admin: True or False depending on if running as admin
    """
    #TODO: vagrant ssh-config gives these details, we can read them and strip them out automatically

    env.vagrant_instance = True
    settings_file_path = 'settings/vagrant.ini'
    define_env(settings_file_path)

    if admin:
        env.user = get_config('admin_user')

    env.hosts = [get_config('host')]
    env.port = get_config('host_ssh_port')

@task(alias='s')
def stage(admin=False):
    """
    Set up deployment for staging server

    admin: True or False depending on if running as admin
    """

    define_env()
    if admin:
        env.user = get_config('admin_user')

    env.hosts = get_config('staging_host')
    #env.port = ### #Uncomment this line if a specific port is required

@task(alias='p')
def prod(admin=False):
    """
    Set up deployment for production server

    admin: True or False depending on if running as admin
    """

    define_env()
    if admin:
        env.user = get_config('admin_user')

    env.hosts = get_config('production_host')
    #env.port = ### #Uncomment this line if a specific port is required

#TODO create restore backup function


@task
def deploy(name):
    """
    This function does all the work required to ship code to the
    server being deployed to.

    version: the version applied to the tag of the release
    """
    make_upload_target()
    upload_package_and_extract(name)
    update_redcap_connection()
    write_remote_my_cnf()
    create_redcap_tables()
    move_software_to_live()
    move_edocs_folder()
    set_redcap_base_url()
    set_hook_functions_file()
    configure_redcap_cron()
    #TODO: Run tests, run django validation


"""
The following functions are admin level functions which will alter the server.
They will need to be run with the admin=True flag when setting up the env
"""

@task
def setup_webspace():
    """
    make www and www.backup directory as admin or root user

    Note: Admin must be true in the environment
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
    This function creates the deploy user and sets up the directories being used for the project
    Note: Admin must be true in the environment
    """
    create_deploy_user_with_ssh()
    setup_webspace()

@task(alias='cduws')
def create_deploy_user_with_ssh():
    """
    This function will ssh in with the assigned admin user account,
    prompt for password, and create the deployment user. It will place
    this user in the group assigned.

    Note: If ssh is locked to specific users, make sure to add this
    new user to that list
    Note: Admin must be true in the environment
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
    This function makes the deploy user owner of these documents and locks down
    other permissions
    """

    #create SSH directory
    with settings(user=env.deploy_user):
        run('chmod 700 /home/%s/.ssh' % env.deploy_user)
        run('chmod 644 /home/%s/.ssh/authorized_keys' % env.deploy_user)
        run('chmod -R 700 /home/%s/.ssh/keys' % env.deploy_user)
        #run('chown -R %s.%s /home/%s' % (env.deploy_user, env.deploy_group, env.deploy_user))

@task(alias='ssh_string')
def add_new_ssh_key_as_string(ssh_public_key_string, name):
    """
    This function will add the passed ssh key string to the deploy user to enable
    passwordless login
    Note: Admin must be true in the environment
    TODO: validate string is valid ssh key

    ssh_public_key_string: the actual public key string
    name: the name of the user this key is tied to
    """

    ssh_key = ssh_public_key_string
    copy_ssh_key_to_host(ssh_key,name)
    rebuild_authorized_keys()
    update_ssh_permissions()

@task(alias='ssh_file')
def add_new_ssh_key_as_file(ssh_public_key_path, name):
    """
    This function will copy the ssh key from a local file to the deploy user to enable
    passwordless login
    Note: Admin must be true in the environment

    ssh_public_key_string: the actual public key full file path
    name: the name of the user this key is tied to
    """
    ssh_key = open(ssh_public_key_path, 'r').read()
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
