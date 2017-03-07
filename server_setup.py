from fabric.api import *
from fabric.contrib.files import exists
from fabric.utils import abort
import string, random


def setup_webspace():
    """
    Make live web space (e.g., www) and backup web space (e.g. www.backup) as root user
    """
    # Change the permissions to match the correct user and group
    sudo("mkdir -p %(backup_project_full_path)s" % env)

    sudo("chown -R %s.%s %s" % (env.deploy_user, env.deploy_group, env.backup_pre_path))
    sudo("chmod -R 775 %s" % env.backup_pre_path)

    sudo("chown -R %s.%s %s" % (env.deploy_user, env.deploy_group, env.live_pre_path))
    sudo("chmod -R 775 %s" % env.live_pre_path)

    sudo("mkdir -p %s" % env.edoc_path)
    sudo("chown -R %s.%s %s" % (env.deploy_user, env.deploy_group, env.edoc_path))
    sudo("chmod -R 775 %s" % env.edoc_path)


@task(default=True)
def setup_server():
    """
    Create the 'deploy' user and set up the web space and backup web space
    """
    create_deploy_user_with_ssh()
    setup_webspace()


@task
def create_deploy_user_with_ssh():
    """
    Create 'deploy' user as root.

    This function will create the deployment user. It will place
    this user in the group assigned.
    """

    random_password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32))

    # Make a deploy user with the right group membership
    with settings(warn_only=True):
        if sudo('getent passwd %s > /dev/null' % env.deploy_user).return_code == 0:
            sudo('usermod -g %s %s' % (env.deploy_group, env.deploy_user))
        else:
            sudo('useradd -m -b /home -u 800 -g %s -s /bin/bash -c "deployment user" %s -p %s' \
                % (env.deploy_group, env.deploy_user, random_password))

    with settings(warn_only=True):
        if sudo('test -d ~%s/.ssh/keys' % env.deploy_user).failed:
            sudo('mkdir -p ~%s/.ssh/keys' % env.deploy_user)
            path_to_authorized_keys = "~%s/.ssh/authorized_keys" % env.deploy_user
            if sudo("test -e %s" % path_to_authorized_keys).succeeded:
                sudo('cp %s ~%s/.ssh/keys/default.pub' % (path_to_authorized_keys, env.deploy_user))
            else:
                sudo("touch %s" % path_to_authorized_keys)
            path_to_new_pub_key = "/home/%(deploy_user)s/.ssh/keys/%(user)s.pub" % env
            put(env.pubkey_filename, path_to_new_pub_key, use_sudo=True)
            sudo("cat %s >> %s" % (path_to_new_pub_key, path_to_authorized_keys))
            sudo("chown -R %s.%s ~%s/.ssh" % (env.deploy_user, env.deploy_group, env.deploy_user))

    update_ssh_permissions(as_root=True)

    # TODO: automatically add ssh key or prompt


def update_ssh_permissions(as_root=False):
    """
    Adjust perms on the 'deploy' user's ssh keys
    """

    if as_root:
        sudo('chmod 700 /home/%s/.ssh' % env.deploy_user)
        sudo('chmod 644 /home/%s/.ssh/authorized_keys' % env.deploy_user)
        sudo('chmod -R 700 /home/%s/.ssh/keys' % env.deploy_user)
    else:
        with settings(user=env.deploy_user):
            run('chmod 700 /home/%s/.ssh' % env.deploy_user)
            run('chmod 644 /home/%s/.ssh/authorized_keys' % env.deploy_user)
            run('chmod -R 700 /home/%s/.ssh/keys' % env.deploy_user)
            # run('chown -R %s.%s /home/%s' % (env.deploy_user, env.deploy_group, env.deploy_user))


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
