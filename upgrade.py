from fabric.api import *
from datetime import datetime
import re
import fnmatch
import utility
import utility_redcap


@task(default=True)
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
    # run the tests but take REDCap offline again and abort if they fail
    if not utility_redcap.test(warn_only=True):
        offline()
        utility.delete_remote_my_cnf()
        abort("One or more tests failed.  REDCap has been taken offline.")
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


def apply_incremental_db_changes(old, new):
    """
    Upgrade the database from the <old> REDCap version to the <new> version.

    Done by applying the needed upgrade_M.NN.OO.sql and upgrade_M.NN.OO.php
    files in sequence. The arguments old and new must be version numbers (i.e., 6.11.5)
    """
    old = utility.convert_version_to_int(old)
    new_as_an_int = utility.convert_version_to_int(new)
    redcap_sql_dir = '/'.join([env.live_pre_path, env.project_path, 'redcap_v' + new, 'Resources/sql'])
    with settings(user=env.deploy_user):
        with hide('output'):
            files = run('ls -1 %s/upgrade_*.sql %s/upgrade_*.php  | sort --version-sort ' % (redcap_sql_dir, redcap_sql_dir))
    path_to_sql_generation = '/'.join([env.live_pre_path, env.project_path, 'redcap_v' + new, 'generate_upgrade_sql_from_php.php'])
    for file in files.splitlines():
        match = re.search(r"(upgrade_)(\d+.\d+.\d+)(.)(php|sql)", file)
        version = match.group(2)
        version = utility.convert_version_to_int(version)
        if version > old and version <= new_as_an_int:
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


def offline():
    change_online_status('Offline')


def online():
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