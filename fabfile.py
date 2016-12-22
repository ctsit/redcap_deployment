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

config = configparser.ConfigParser()
settings_file_path = 'qipr_approver/deploy/settings.ini' #path to where app is looking for settings.ini

def get_config(key):
    return config.get("fabric_deploy", key)

def define_env():
    """
    This function sets up some global variables
    """

    #first, copy the secrets file into the deploy directory
    if os.path.exists(settings_file_path):
        config.read(settings_file_path)
    else:
        print("The secrets file path cannot be found. It is set to: %s" % settings_file_path)
        abort("Secrets File not set")

    env.user = get_config('deploy_user') #default ssh deploy user account
    env.project_name = get_config('project_name')
    env.project_settings_path = get_config('project_settings_path')
    env.live_project_full_path = get_config('live_pre_path') + "/" + get_config('project_path') #
    env.backup_project_full_path = get_config('backup_pre_path') + "/" + get_config('project_path')
    env.key_filename = get_config('ssh_keyfile_path')

@task(alias='v')
def vagrant(admin=False):
    """
    Set up deployment for vagrant

    admin: True or False depending on if running as admin
    """
    #TODO: vagrant ssh-config gives these details, we can read them and strip them out automatically

    define_env()
    if admin:
        env.user = 'vagrant'
        env.key_filename = '../vagrant/.vagrant/machines/qipr_approver/virtualbox/private_key' #This is the hardcoded vagrant key based on this projects file structure

    env.hosts = ['127.0.0.1']
    env.port = '2222'

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

@task
def git_version(version):
    """
    Pulls the requested version from Master for deployment

    version: the version applied to the tag of the release
    Assumptions:
    git is installed and configured
    Master branch contains releases with the version number as a tag
    """

    local("git stash save 'Stashing current changes while releasing version %s'" % version)
    local("git fetch --all; git checkout %s" % (version))

def package_files():
    """
    This function will go into the project directory and zip all
    of the required files
    """
    #pull out file name for reuse
    env.package_name = '%(project_name)s-%(project_version)s.tar.gzip' % env

    #create the package
    local("tar -cz --exclude='__pycache__' --exclude='.DS_Store' \
    -f %(package_name)s \
    venv/ \
	manage.py \
	qipr_approver/deploy/settings.ini \
    qipr_approver/__init__.py \
    qipr_approver/migration_urls.py \
    qipr_approver/settings.py \
    qipr_approver/urls.py \
    qipr_approver/wsgi.py \
	approver/ \
	static/" % env)

def create_backup():
    """
    This function creates a backup of the current live directory using the project name and current time
    """
    with cd("%(backup_project_full_path)s" % env):
        run("mkdir -p backup")
        if exists('live'):
            run("tar -cz -f backup/%s-%s.tar.gzip live" % (env.project_name, datetime.now().strftime("%Y%m%dT%H%M%Z")))

#TODO create restore backup function

def unpackage_files():
    """
    Unpackage the file in the remote backup directory
    """
    with cd("%(backup_project_full_path)s" % env):
        run("mkdir -p archive/%(project_name)s-%(project_version)s" % env)
        run("tar -x -C archive/%(project_name)s-%(project_version)s \
            -f %(project_name)s-%(project_version)s.tar.gzip" % env)

def link_to_live():
    """
    This function creates a symlink from the backup to the live www directory for the server
    to run the app from.
    """
    run("ln -sf -T %(backup_project_full_path)s/archive/%(project_name)s-%(project_version)s \
    %(live_project_full_path)s" % env)

def refresh_server():
    """
    Touchs the wsgi file to have the server reload the necessary files
    This may not be needed since we are overwriting the files anyways
    """
    run("touch %(live_project_full_path)s/%(project_settings_path)s/wsgi.py" % env)

def ship_to_host():
    """
    Move the zip file to the correct remote directory
    """
    put('%(project_name)s-%(project_version)s.tar.gzip' % env, '%(backup_project_full_path)s' % env)

def clean_up():
    #clean up local files
    local('rm %(project_name)s-%(project_version)s.tar.gzip' % env)

    #clean up remote files
    run('rm %(backup_project_full_path)s/%(project_name)s-%(project_version)s.tar.gzip' % env)

@task
def deploy(version):
    """
    This function does all the work required to ship code to the
    server being deployed to.

    version: the version applied to the tag of the release
    """

    env.project_version = version

    git_version(version)
    package_files()
    ship_to_host()
    create_backup()
    unpackage_files()
    link_to_live()
    refresh_server()
    #TODO: Run tests, run django validation
    clean_up()

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
    sudo("mkdir -p %(live_project_full_path)s" % env)
    sudo("mkdir -p %(backup_project_full_path)s/archive" % env)

    #Change the permissions to match the correct user and group
    sudo("chown -R %s.%s /var/www.backup" % (get_config('deploy_user'), get_config('deploy_user_group')))
    sudo("chmod -R 755 /var/www.backup")

    sudo("chown -R %s.%s /var/www" % (get_config('deploy_user'), get_config('deploy_user_group')))
    sudo("chmod -R 755 /var/www/")

@task
def setup_server():
    """
    This function creates the deploy user and sets up the directories being used for the project
    Note: Admin must be true in the environment
    """
    create_deploy_user_with_ssh()
    setup_webspace()

@task
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
    deploy_user = get_config('deploy_user')
    deploy_user_group = get_config('deploy_user_group')
    sudo('useradd -m -b /home -u 800 -g %s -s /bin/bash -c "deployment user" %s -p %s' % (deploy_user_group, deploy_user, random_password))

    #create SSH directory
    sudo('mkdir -p /home/%s/.ssh/keys' % deploy_user)
    update_ssh_permissions()

    #TODO: automatically add ssh key or prompt

def update_ssh_permissions():
    """
    This function makes the deploy user owner of these documents and locks down
    other permissions
    """
    deploy_user = get_config('deploy_user')

    sudo('chmod 700 /home/%s/.ssh' % deploy_user)
    sudo('chmod 644 /home/%s/.ssh/authorized_keys' % deploy_user)
    sudo('chmod -R 700 /home/%s/.ssh/keys' % deploy_user)
    sudo('chown -R %s.%s /home/%s' % (deploy_user, get_config('deploy_user_group'), deploy_user))

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
    pub_file = open('%s.pub' % name, 'w')
    pub_file.write(ssh_key)
    pub_file.close()
    put('%s.pub' % name, '/home/%s/.ssh/keys/' % get_config('deploy_user'), use_sudo=True)
    #sudo("echo %s >> /home/%s/.ssh/keys/%s.pub" % (, get_config('deploy_user'), name))

def rebuild_authorized_keys():
    """
    Take all the current pub files and recreate authorized_keys from them.
    If any of the pub files are removed, they get removed from the authorized keys
    and can no longer ssh in.
    """
    sudo('sudo cat `sudo find /home/%s/.ssh/keys/ -type f` > tmpfile' % get_config('deploy_user'))
    sudo('cp tmpfile /home/%s/.ssh/authorized_keys' % get_config('deploy_user'))
    sudo('rm tmpfile')
