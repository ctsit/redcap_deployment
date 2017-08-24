from fabric.api import *
from tempfile import mkstemp
import os
import utility
try:
    import configparser
except:
    from six.moves import configparser

__all__ = []


def get_current_redcap_version():
    """
    gets the current redcap version from database
    """
    with settings(user=env.deploy_user):
        with hide('output'):
            current_version = run('mysql -s -N -e "SELECT value from redcap_config WHERE field_name=\'redcap_version\'"')
    return current_version


def make_upload_target():
    """
    Make the directory from which new software will be deployed,
    e.g., /var/www.backup/redcap-20160117T1543/
    """
    env.upload_target_backup_dir = '/'.join([env.upload_project_full_path, env.remote_project_name])
    with settings(user=env.deploy_user):
        run("mkdir -p %(upload_target_backup_dir)s" % env)


def upload_package_and_extract(name):
    """
    Upload the redcap package and extract it into the directory from which new
    software will be deployed, e.g., /var/www.backup/redcap-20160117T1543/
    """
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
        # make sure the temp file directory in redcap web space will be writeable
        run('chmod g+w %s/temp' % env.upload_target_backup_dir)
        # Remove the temp directories
        run('rm -rf %s %s' % (temp1, temp2))


def move_software_to_live():
    """
    Replace the symbolic link to the old code with symbolic link to new code.
    """
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


def test(warn_only=False):
    """
    Run all tests against a running REDCap instance
    """
    utility.write_remote_my_cnf()
    version = get_current_redcap_version()
    utility.delete_remote_my_cnf()
    local("python tests/test.py %s/ redcap_v%s/" % (env.url_of_deployed_app,version))
    with settings(warn_only=True):
        if local("python tests/test.py %s/ redcap_v%s/" % (env.url_of_deployed_app,version)).failed:
            if warn_only:
                warn("One or more tests failed.")
                return(False)
            else:
                abort("One or more tests failed.")
        else:
            return(True)


def deploy_external_modules(relative_path_to_install_sql="external_modules/sql/create\ tables.sql"):
    """
    Run the external_modules/create tables.sql file to build its tables
    """
    absolute_path_to_install_sql = '/'.join([env.live_project_full_path, relative_path_to_install_sql])
    utility.apply_remote_sql_to_db(absolute_path_to_install_sql)


